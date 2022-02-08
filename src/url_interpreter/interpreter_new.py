from typing import Any, List, Optional, Dict

import httpx
from sqlalchemy import sql, String, INT

# How to get column type
# self.dialect_DB().entity_class.ano_referencia.property.columns[0].type
from src.orm.action_type import Action
from src.orm.converter import ConverterType
from src.orm.database import DialectDatabase
from src.orm.dictionary_actions import ActionFunction, dic_action
from src.orm.models import AlchemyBase
from src.url_interpreter.expression import Expression
from src.url_interpreter.interpreter_error import PathError
from src.url_interpreter.state_machine import StateMachineNew
from src.url_interpreter.token import Token, TokenAttribute, TokenIn, TokenAnd, TokenOr, TokenBetween, TokenOperation, \
    TokenArg, TokenInArg, TokenParenthese, TokenValue, TokenRelationalOperator
from src.url_interpreter.tword import TWord
from ..hyper_resource.common_resource import *
from ..hyper_resource.util import get_request

dict_relational_operator = {
    'gt': '>',
    'lt': '<',
    'eq': '=',
    'neq': '<>',
    'gte': '>=',
    'lte': '<='
}
dict_null_operator = {
    'isnull': ' is null ',
    'isnotnull': ' is not null '
}
dict_logical_operator = {
    'and': ' and ',
    'nand': ' not and ',
    'or': ' or ',
    'nor': ' not or '
}
dict_parentheses_word = {
    '(': ' ( ',
    ')': ' ) ',
}
dict_in_operator = {  # geocode in ('UK', 'US', 'JP')
    'in': ' in ',
    'notin': ' not in '
}


def convert_data(data: Any, typeof: type) -> Any:
    if typeof == str or typeof == String:
        data = data.strip()
        if data.startswith("'") and data.endswith("'"):
            return data
        return f"'{data}'"
    elif typeof == int or typeof == INT:
        return int(data)
    elif typeof == float:
        return float(data)
    else:
        return data


def convert_data_in_enum(data: Any, data_type: str) -> str:
    if data_type.startswith('VARCHAR'):
        values = data.split(',')
        if data.startswith("'") and data.endswith("'"):
            return data
        return ",".join([f"'{value}'" for value in values])

    elif data_type.startswith('INTEGER'):
        return data
    else:
        return data


def as_enum(list: List):
    return ','.join(list)


def path_has_url(path: str) -> bool:
    return '/(/http:' in path or '/(/https:' in path


def path_with_url_splitted(path: str) -> List[str]:
    """
    :param path must have an url> example: geom/contains/(/http://unidade-federacao/rj/geom/)/
    :return: List[str]
    """
    idx_ini = path.find('/(/http')
    if idx_ini == -1:
        raise SyntaxError(f"Problem with {path}. Verify if path has balanced parentheses and http")
    first_part_lst = (path[0:idx_ini]).split('/')
    idx_midst = path.find('/)', idx_ini)
    if idx_midst == -1:
        raise SyntaxError(
            f"Problem with {path}. Verify if path has balanced parentheses ---'/(/'---'/)/'---  and http")
    middle_part_lst = (path[idx_ini + 3:idx_midst])
    return first_part_lst + [middle_part_lst]


def path_as_list(path: str) -> List[str]:
    if path[-1] == '/':  # Removes trail slash
        path = path[:-1]
    if path_has_url(path):
        return path_with_url_splitted(path)
    return path.split('/')


class InterpreterNew:
    def __init__(self, an_expression: str, model_class: AlchemyBase, dialect_db: DialectDatabase):
        self.expression: Expression = Expression(an_expression)
        self.model_class = model_class
        self.state_machine = StateMachineNew()
        self.dialect_db = dialect_db
        self.tokens: Optional[List[Token]] = None
        self.token = None

    def twords(self) -> List[TWord]:
        return self.expression.twords()

    def words(self) -> List[str]:
        return self.expression.words()

    def prev_token(self, a_token: Optional[Token] = None, index: int = 0) -> Optional[Token]:
        if a_token is not None:
            idx: int = self.tokens.index(a_token)
            if idx == 0:
                return None
            return self.tokens[idx - 1]
        if index == 0:
            return None
        if index == 3:
            print(self.tokens)
        print("INDEX: ", index)
        print("self.tokens: ", len(self.tokens))
        return self.tokens[index - 1]

    def word_is_url(self, a_word: str) -> bool:
        return a_word.lower() == 'http:' or a_word.lower() == 'https:' or a_word.lower() == 'www.'

    def word_is_not_url(self, a_word: str) -> bool:
        return not self.word_is_url(a_word)

    def word_is_attribute(self, tk: str) -> bool:
        return self.model_class.has_attribute(tk)

    def word_is_relational_operator(self, tk: str) -> bool:
        return tk in dict_relational_operator

    def word_is_null_operator(self, tk: str) -> bool:
        return tk in dict_null_operator

    async def word_is_operation(self, word: str, prv_token: Optional[Token] = None) -> bool:
        if prv_token is None:
            return False
        a_type = await prv_token.returned()
        return a_type in self.dict_action() and (word in self.dict_action()[a_type])

    async def word_is_operation_arg(self, a_word: str, prv_token: Token) -> bool:
        if prv_token is None:
            msg_error = f'Must have a function name before {self.token.word()}'
            print(msg_error)
            raise PathError(msg_error, 400)
        if prv_token.is_not_operation():
            return False
        an_action: ActionFunction = self.dialect_db_action(prv_token.typeof, prv_token.word())

        return an_action.has_parameters()

    def word_is_in_arg(self, prv_token: Token) -> bool:
        if prv_token is None:
            return False
        return prv_token.word() == Token.IN_OPERATOR

    def word_is_logical_operator(self, tk: str) -> bool:
        return tk in dict_logical_operator

    def word_is_in_operator(self, tk: str) -> bool:
        return tk in dict_in_operator

    def word_is_parentheses(self, tk: str) -> bool:
        return tk in dict_parentheses_word

    async def next_token(self, a_token: Optional[Token], idx: Optional[int] = None) -> Optional[Token]:
        if a_token is None:
            return None
        _twords: List[TWord] = self.twords()
        index: int = idx + 1 if idx is not None else _twords.index(a_token.tword) + 1
        if index > len(_twords):
            return None
        _tword: TWord = _twords[index]
        return await self.get_token_given(_tword, a_token)

    def set_next_token_on_token(self, tk: Token, prv_token: Optional[Token]) -> Token:
        if prv_token:
            prv_token.next_token = tk
        return tk

    async def get_token_given(self, tword: Optional[TWord], prv_token: Optional[Token]):
        if self.word_is_attribute(tword.word):
            tk = TokenAttribute(tword, Token.ATTRIBUTE_CATEGORY, self.type_of_attribute(tword.word), prv_token)
            return self.set_next_token_on_token(tk, prv_token)
        elif self.word_is_relational_operator(tword.word):
            tk = TokenRelationalOperator(tword, Token.RELATIONAL_OPERATOR_CATEGORY, str, prv_token)
            return self.set_next_token_on_token(tk, prv_token)
        elif self.word_is_in_operator(tword.word) and prv_token is not None:
            tp: type = await prv_token.returned()
            tk = TokenIn(tword, Token.IN_OPERATOR, tp,  prv_token)
            return self.set_next_token_on_token(tk, prv_token)
        elif tword.word == Token.AND_CATEGORY:
            tk = TokenAnd(tword, Token.AND_CATEGORY, str,  prv_token)
            return self.set_next_token_on_token(tk, prv_token)
        elif tword.word == Token.OR_CATEGORY:
            tk = TokenOr(tword, Token.OR_CATEGORY, str,  prv_token)
            return self.set_next_token_on_token(tk, prv_token)
        elif tword.word == Token.BETWEEN_CATEGORY:
            tk = TokenBetween(tword, Token.BETWEEN_CATEGORY, str,  prv_token)
            return self.set_next_token_on_token(tk, prv_token)
        elif tword.word == Token.PAREN_OPEN:
            tk = TokenParenthese(tword, Token.PAREN_OPEN, str,  prv_token)
            return self.set_next_token_on_token(tk, prv_token)
        elif tword.word == Token.PAREN_CLOSE:
            tk = TokenParenthese(tword, Token.PAREN_CLOSE, str,  prv_token)
            return self.set_next_token_on_token(tk, prv_token)
        elif prv_token is not None and await self.word_is_operation(tword.word, prv_token):
            a_type = await prv_token.returned()
            action = self.dialect_db_action(a_type, tword.word)
            tk = TokenOperation(tword, Token.OPERATION_CATEGORY, a_type, prv_token, action.answer)
            return self.set_next_token_on_token(tk, prv_token)
        elif await self.word_is_operation_arg(tword.word, prv_token) and prv_token is not None:
            a_type = prv_token.typeof
            # action = self.dialect_db_action(a_type, tword.word)
            tk = TokenArg(tword, Token.OPERATION_ARG_CATEGORY, str, prv_token)
            return self.set_next_token_on_token(tk, prv_token)
        elif self.word_is_in_operator(prv_token.word()) :
            tk = TokenInArg(tword, Token.IN_OPERATOR_ARG, str, prv_token)
            return self.set_next_token_on_token(tk, prv_token)
        else:
            tp = await prv_token.returned() if prv_token is not None else None
            tk = TokenValue(tword, Token.VALUE_CATEGORY, tp,  prv_token)
            return self.set_next_token_on_token(tk, prv_token)

    async def get_tokens(self) -> List[Token]:
        if self.tokens:
            return self.tokens
        self.tokens = [None]*len(self.twords())
        prv_token: Optional[Token] = None
        for idx, tword in enumerate(self.twords()):
            if idx > 0:
                prv_token = self.tokens[idx - 1]
            _token: Token = await self.get_token_given(tword, prv_token)
            self.tokens[idx] = _token
        return self.tokens

    def type_of_attribute(self, attr_name: str) -> type:
        """
        returns the type of the attribute in a Model class. This method expects a name of attribute in a Model class
        :param attr_name:is attribute defined at a Model class hierarchy
        :return: type
        """
        return self.model_class.attribute_type_given(attr_name)

    def dialect_db_action(self, typeof: object, word: str):
        return self.dialect_db.action(typeof, word)

    def dict_action(self) -> Dict[str, ActionFunction]:
        return self.dialect_db.dict_action()

    async def action_function(self, a_token: Optional[Token] = None) -> Optional[ActionFunction]:
        tk: Token = a_token or self.token
        prev_tk: Optional[Token] = self.prev_token(tk)
        if prev_tk is None:
            raise PathError(f'Error in the path. See path before {tk.word()}', 400)

        #prev_tk = prev_tk.token_parent if prev_tk.is_operation_arg() else prev_tk

        return self.dialect_db_action( await prev_tk.returned(), tk.word())

    def action_from_operation(self, a_token: Token, operation_name: str) -> ActionFunction:
        return dic_action[a_token.typeof][operation_name]

    def returned_type_of_operation(self, a_token: Token, operation_name: str) -> object:
        action: ActionFunction = self.action_from_operation(a_token, operation_name)
        return action.answer

    async def convert_value(self, token: Token, token_index: int):

        if self.word_is_url(token.word()):
            req = await get_request(token.word())
            if req.status_code == 200:
                res = req.json()
            else:
                raise IOError(f"Error in request: {token}")
        prv_token = self.prev_token(index=token_index)
        if prv_token is not None and prv_token.word() == Token.IN_OPERATOR:
            converted_list = []
            words: List[str] = token.word().split(",")
            for value in words:
                converted_list.append(convert_data(value, token.typeof))
            return "(" + ",".join(converted_list) + ")"
        if prv_token is not None and self.word_is_relational_operator(prv_token.word()):
            prv_prv_token: Token = self.prev_token(index=token_index - 1)
            tp = await prv_prv_token.returned()
            return convert_data(token.word(), tp)
        return convert_data(token.word(), token.typeof)

    async def convert_parameters_for_args(self, params: List[str], action: ActionFunction) -> List:
        return await ConverterType().convert_parameters(params, action.param_types())

    async def translate_for_attribute(self, translated: str) -> str:
        tuple_attrib_column_type = self.model_class.attribute_column_type(self.token.word())
        translated += tuple_attrib_column_type[1]
        return translated

    def translate_for_logical_operator(self, translated: str) -> str:
        translated += dict_logical_operator[self.token.word()]
        return translated

    # attribute_name: str, attribute_type: str,
    async def translate_for_in_operator(self, translated: str) -> str:
        translated += dict_in_operator[self.token.word()]
        return translated

    async def translate_for_operation(self, translated: str) -> str:
        # filter/geom/transform/3005/buffer/1.2/within/https://servergeo/api/states/RJ
        # where st_within(st_buffer(st_transform(geom, 3005),1.2), https://servergeo/api/states/RJ)
        action: ActionFunction = await self.action_function()
        if action is None:
            return ''
        prev_tk = self.prev_token(self.token)
        if prev_tk.is_attribute():
            if action.has_not_parameters():
                return f'{action.name}({self.model_class.column_name(prev_tk.word())})'
            else:
                return f'{action.name}({self.model_class.column_name(prev_tk.word())}, '
        elif prev_tk.is_operation() or prev_tk.is_operation_arg():
            if action.has_not_parameters():
                return f'{action.name}({translated})'
            else:
                return f'{action.name}({translated}, '
        return translated

    def validate_translate_for_operation_arg(self, action: ActionFunction, prev_tk: Token):
        if prev_tk is None:
            raise PathError(f'Error in the path. Before {self.token.word()} must be a function', 400)
        if prev_tk.is_not_operation():
            raise PathError(f'Error in the path. {prev_tk.word()} must be a function', 400)
        if action.has_not_parameters():
            raise PathError(f'Error in the path. {self.token.word()} must be parameters in function {prev_tk.word()}',
                            400)
        if self.token.is_not_operation_arg():
            raise PathError(f'Error in the path. {self.token.word()} must be a arguments of function: {prev_tk.word()}',
                            400)

    async def translate_for_operation_arg(self, translated: str) -> str:
        prev_tk = self.prev_token(self.token)
        action: ActionFunction = self.dialect_db_action(prev_tk.typeof, prev_tk.word())
        if action is None:
            return ''
        self.validate_translate_for_operation_arg(action, prev_tk)
        params: List[str] = self.token.word().split('&')
        converted_parameters = await self.convert_parameters_for_args(params, action)
        params_as_enum = ''.join([f'{para}' for para in converted_parameters])
        return translated + params_as_enum + ')'

    async def translate_for_relational_operator(self, attribute_name: str, attribute_type: str, translated: str) -> str:
        translated += dict_relational_operator[self.token.word()]  # prev word could be an attribute or function

        return translated

    def translate_url_as_word(self) -> str:
        pass

    def translate_for_parantheses_word(self, translated: str) -> str:
        translated += dict_parentheses_word[self.token.word()]
        return translated

    async def is_last_token_operation_without_arg(self) -> bool:
        nxt_token: Optional[Token] = await self.next_token(self.token)
        if nxt_token is None:
            return True
        if nxt_token.is_operation_arg():
            return False
        return nxt_token.is_not_operation()

    async def is_last_token_operation_with_arg(self) -> bool:
        nxt_token: Optional[Token] = await self.next_token(self.token)
        return nxt_token.is_not_operation()

    async def translate(self) -> str:
        # getattr(self.modelClass, "somar_ano").__annotations__
        translated = ''
        tk = ''  # first state
        token_category = None
        twords: List[TWord] = self.twords()
        index = 0
        stack_token_operation: List[Token] = []
        translated_operation = ''
        while index < len(twords):
            tword: TWord = twords[index]
            #tk = self.get_token_given(tword, self.prev_token(index=index))
            tks: List[Token] = await self.get_tokens()
            tk = tks[index]
            self.token = tk
            #self.get_tokens().append(tk)
            token_category = tk.category
            try:
                self.state_machine.set_next_state(tk, tk.category)
            except ValueError:
                if self.state_machine.is_final_state():
                    return translated
                else:
                    raise SyntaxError("Sintaxe error in URL")

            if token_category == Token.ATTRIBUTE_CATEGORY:
                nxt_token: Token = await self.next_token(self.token)
                if nxt_token.is_not_operation():
                    translated = await self.translate_for_attribute(translated)
            elif token_category in [Token.OR_CATEGORY, Token.AND_CATEGORY]:  # todo: not supporting NAND nor NOR
                translated = self.translate_for_logical_operator(translated)
            elif token_category in [Token.PAREN_OPEN, Token.PAREN_CLOSE]:
                translated = self.translate_for_parantheses_word(translated)
            elif token_category == Token.RELATIONAL_OPERATOR_CATEGORY:
                translated += dict_relational_operator[self.token.word()]
            elif token_category in [Token.IN_OPERATOR]:
                translated = await self.translate_for_in_operator(translated)
            elif token_category == Token.OPERATION_CATEGORY:  # self.word_is_operation(tk.word()):
                translated_operation = await self.translate_for_operation(translated_operation)
                is_last = self.is_last_token_operation_without_arg()
                if is_last:
                    translated += translated_operation
                    translated_operation = ''
            elif token_category == Token.OPERATION_ARG_CATEGORY:
                translated_operation = await self.translate_for_operation_arg(translated_operation)
                if self.is_last_token_operation_with_arg():
                    translated += translated_operation
                    translated_operation = ''

            elif token_category == Token.VALUE_CATEGORY or token_category == Token.IN_OPERATOR_ARG:
                a_value = await self.convert_value(tk, index)
                translated += f'{a_value}'
            index += 1
        return translated

    async def translate_lookup(self): #geom/transform/3005/area/gt/100000
        tks: List[Token] = await self.get_tokens()
        tk: Token = tks[0]
        translated_to_where_db: str = ''
        translated_operation: str = ''
        while tk:
            self.state_machine.set_next_state(tk, tk.category)
            if tk.is_operation():
                translated_operation = await tk.translate(translated_operation, self.model_class, self.dialect_db)
                if tk.is_last_operation():
                    translated_to_where_db += translated_operation
                    translated_operation = ''
                if tk.next_token is not None and tk.next_token.is_operation_arg():
                    tk = tk.next_token
            else:
                translated_to_where_db += await tk.translate(None, self.model_class, self.dialect_db)
            tk = tk.next_token
        print(translated_to_where_db)
        return translated_to_where_db

    async def translate_in_query(self, path: str) -> str:

        paths: List[str] = path.split('.')
        expressions: List[Expression] = [Expression(a_path) for a_path in paths]



