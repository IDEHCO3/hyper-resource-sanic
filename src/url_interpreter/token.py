from typing import Optional, List

import aiohttp

from src.hyper_resource.common_resource import CONTENT_TYPE_JSON
from src.orm.action_type import ActionFunction
from src.orm.converter import ConverterType
from src.orm.database import DialectDatabase
from src.orm.models import AlchemyBase
from src.url_interpreter.interpreter_error import PathError
from src.url_interpreter.tword import TWord


class Token:
    ATTRIBUTE_CATEGORY = "attribute"
    RELATIONAL_OPERATOR_CATEGORY = "relational_operator"
    IN_OPERATOR = "in"
    IN_OPERATOR_ARG = "in_arg"
    VALUE_CATEGORY = "value"
    AND_CATEGORY = "and"
    OR_CATEGORY = "or"
    BETWEEN_CATEGORY = "between"
    OPERATION_CATEGORY = "operation"
    OPERATION_ARG_CATEGORY = "operation_arg"
    PAREN_OPEN = "("
    PAREN_CLOSE = ")"
    dict_relational_operator = {
        'gt': '>',
        'lt': '<',
        'eq': '=',
        'neq': '<>',
        'gte': '>=',
        'lte': '<='
    }

    def __init__(self, tword: TWord, category: str, tpe: Optional[type] = None, prev_token: Optional['Token'] = None):
        self.tword = tword
        self.category = category
        self.typeof = tpe
        self.prev_token = prev_token
        self.next_token: Optional[Token] = None

    def word(self) -> str:
        return self.tword.word

    def is_operation(self) -> bool:
        return self.category == Token.OPERATION_CATEGORY

    def is_not_operation(self) -> bool:
        return not self.is_operation()

    def is_operation_arg(self) -> bool:
        return self.category == Token.OPERATION_ARG_CATEGORY

    def is_not_operation_arg(self) -> bool:
        return not self.is_operation_arg()

    def is_attribute(self) -> bool:
        return self.category == Token.ATTRIBUTE_CATEGORY

    def is_last_operation(self):
        return True

    def has_url(self) -> bool:
        return self.tword.is_url()

    def value_has_url(self, value_str: str) -> bool:
        return (value_str.find('http:') > -1) or (value_str.find('https:') > -1) or (value_str.find('www.') > -1)

    def __repr__(self):
        return self.word()

    async def returned(self) -> Optional[type]:
        return self.typeof

    async def translate(self, translated: str = None, model_class: Optional[AlchemyBase] = None, db: Optional[DialectDatabase] = None) -> str:
        return f'{self.word()} '

    async def request(self, url: str, accept: str = CONTENT_TYPE_JSON):
        headers = {'accept': accept}
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                _json = await resp.json()
                return _json

class TokenAttribute(Token):

    def is_attribute(self) -> bool:
        return True

    async def returned(self) -> type:
        return self.typeof

    def column_name(self, model_class: Optional[AlchemyBase]):
        return model_class.attribute_column_type(self.word())[1]

    async def translate(self, translated: str = None, model_class: Optional[AlchemyBase] = None, db: Optional[DialectDatabase] = None) -> str:
        if self.next_token and self.next_token.is_operation():
            return ''
        return f'{self.column_name(model_class)} '

class TokenOperation(Token):
    def __init__(self, tword: TWord, category: str, tpe: Optional[type] = None, prev_token: Optional['Token'] = None,
                 return_type: Optional[type] = None):
        super(TokenOperation, self).__init__(tword, category, tpe, prev_token)
        self.return_type = return_type
        self._translated: Optional[str] = None

    def is_operation(self) -> bool:
        return True

    def is_last_operation(self) -> bool:
        if self.next_token is None:
            return True
        if self.next_token.is_not_operation() and self.next_token.is_not_operation_arg():
            return True
        if self.next_token.is_operation_arg():
            if self.next_token.next_token is None:
                return True
            return self.next_token.next_token.is_not_operation()

    async def returned(self) -> type:
        return self.return_type

    async def convert_db_args(self, db: DialectDatabase, params_str: List[str], param_types: List[type]) -> str:
        converted_params: List[str] = []
        for idx, param in enumerate(params_str):
            if self.value_has_url(param):
                res = await self.request(param)
                print(res)
            else:
                res = await db.value_db_converted( param, param_types[idx])
            converted_params.append(f'{res}')
        return ','.join(converted_params)

    async def translate(self, translated: str = None,  model_class: Optional[AlchemyBase] = None, db: Optional[DialectDatabase] = None) -> str:
        tp: type = await self.prev_token.returned()
        action: ActionFunction = db.action(tp, self.word())
        if action is None:
            raise PathError('function {self.token.word()} not exists', 400)
        converted_db_params_str: str = ''
        if action.has_parameters():
            nx_token: Token = self.next_token
            params_str: List[str] = nx_token.word().split('&')
            converted_db_params_str: str = ',' + await db.convert_db_args(params_str, action.param_types())
        if self.prev_token.is_attribute():
            prev_translated = self.prev_token.column_name(model_class)
            return f'{action.name}({prev_translated}{converted_db_params_str})'

        return f'{action.name}({translated}{converted_db_params_str})'


class TokenArg(Token):

    def is_operation_arg(self) -> bool:
        return True

    def is_operation_or_arg(self) -> bool:
        return True

    def is_last_operation(self) -> bool:
        if self.next_token is None:
            return True
        return self.next_token.is_not_operation()

    async def returned(self) -> type:
        return await self.prev_token.returned()

    async def translate(self, translated: str = None,  model_class: Optional[AlchemyBase] = None, db: Optional[DialectDatabase] = None) -> str:
        return ''


class TokenLogicalOperator(Token):

    async def returned(self) -> Optional[type]:
        return str

class TokenOr(TokenLogicalOperator):
    async def translate(self, translated: str = None,  model_class: Optional[AlchemyBase] = None, db: Optional[DialectDatabase] = None) -> str:
        return 'or '


class TokenAnd(TokenLogicalOperator):
    async def translate(self, translated: str = None,  model_class: Optional[AlchemyBase] = None, db: Optional[DialectDatabase] = None) -> str:
        return 'and '


class TokenIn(Token):

    async def translate(self, translated: str = None, model_class: Optional[AlchemyBase] = None,  db: Optional[DialectDatabase] = None) -> str:
        values: str = self.next_token.word()
        a_type = await self.prev_token.returned()
        list_value_converted = await db.convert_in_db_args(values, a_type)
        return f'in ({list_value_converted}) '

    async def returned(self) -> Optional[type]:
        return await self.prev_token.returned()


class TokenInArg(Token):
    async def translate(self, translated: str = None, model_class: Optional[AlchemyBase] = None,  db: Optional[DialectDatabase] = None) -> str:
        return ''

    async def returned(self) -> Optional[type]:
        return await self.prev_token.returned()

class TokenBetween(Token):

    async def translate(self, translated: str = None, model_class: Optional[AlchemyBase] = None,  db: Optional[DialectDatabase] = None) -> str:
        tuple_attrib_column_type = model_class.attribute_column_type(self.word())
        column_name = tuple_attrib_column_type[1]
        params = self.next_token.word().split('&')
        param1 = await db.value_db_converted(params[0], self.typeof)
        param2 = await db.value_db_converted(params[1], self.typeof)
        return f'{column_name} between {param1} and {param2} '


class TokenValue(Token):
    async def translate(self, translated: str = None, model_class: Optional[AlchemyBase] = None,
                        db: Optional[DialectDatabase] = None) -> str:
        tp: type = await self.returned()
        obj = await db.value_db_converted(self.word(), tp)
        return f'{obj} '

    async def returned(self) -> Optional[type]:
        return await self.prev_token.returned()

class TokenRelationalOperator(Token):
    async def translate(self, translated: str = None, model_class: Optional[AlchemyBase] = None,  db: Optional[DialectDatabase] = None) -> str:
        wd: str =  Token.dict_relational_operator[self.word()]
        return f'{wd} '

    async def returned(self) -> Optional[type]:
        return await self.prev_token.returned()

class TokenParenthese(Token):
    async def translate(self, translated: str = None, model_class: Optional[AlchemyBase] = None,
                        db: Optional[DialectDatabase] = None) -> str:
        return f'{self.word()} '