import re
from typing import Dict, Tuple, Sequence, List, Any
import httpx
import pandas as pd
import os
import inspect
from sqlalchemy.orm import Session, aliased

# How to get column type
# self.dialect_DB().entity_class.ano_referencia.property.columns[0].type
from src.url_interpreter.datatype import python_to_sqlalchemy_type


async def get_request(url):
    async with httpx.AsyncClient() as client:
      return await client.get(url)

"""
dict_init = {'s0': {'attribute': 's1', '(': 's2'}}
dict_attribute = {'s1': {'relational_operator': 's3','logical_operator': 's4' ,'null_operator': 's5', 'in_operator':'s6', 'function_operator': 's7'}}
dict_left_parenthese = {'s2': {'attribute': 's1', '(': 's2'}}
dict_relational = {'s3': {'value': 's8', 'value_as_url': 's9'}}
dict_value = {'s10': {None: 'fs', 'logical_operator': 's4', ')':'s11'}}
dict_logical = {'s12': {'value': 's8', 'value_as_url': 's9', ')':'s11'}}
dict_right_parenthese = {'s13': {None: 'sf', ')': 's13', 'relational_operator': 's3', }}
"""

dict_relational_operator = {
    'gt': '>',
    'lt': '<',
    'eq': '=',
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
dict_in_operator = { #geocode in ('UK', 'US', 'JP')
    'in': ' in ',
    'notin': ' not in '
}

def convert_data(data: Any, data_type: str) -> Any:
    if data_type.startswith('VARCHAR'):
        if data.startswith("'") and data.endswith("'"):
            return data
        return f"'{data}'"
    elif data_type.startswith('INTEGER'):
        return str(data)
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

ATTRIBUTE_CATEGORY = "attribute"
RELATIONAL_OPERATOR_CATEGORY = "relational_operator"
IN_OPERATOR = "in"
VALUE_CATEGORY = "value"
AND_CATEGORY = "and"
OR_CATEGORY = "or"
BETWEEN_CATEGORY = "between"
OPERATION_CATEGORY = "operation"
PAREN_OPEN = "("
PAREN_CLOSE = ")"

class StateMachine:
    def __init__(self):
        self.transition_table = pd.read_csv(os.path.join(os.path.dirname(__file__), "state-machine.csv"))
        self.current_state = 0

    def set_next_state(self, token, token_category):
        if token_category == OPERATION_CATEGORY:
            return # keep current state

        new_state = int(self.transition_table[token_category][self.current_state])
        self.current_state = new_state

    def is_final_state(self):
        return self.transition_table["is_final"][self.current_state]

# class Token:
#     types = ['ATTRIBUTE', 'BEGIN_PARENTHESE']
#     def __init__(self, word, type, representation):
#         self.word = word
#         self.type = type
#         self.representation = representation


class Interpreter:
    def __init__(self, an_expression, modelClass):
        self.expression = an_expression[1:] if an_expression[0] == '/' else an_expression
        self.sub_expression = self.expression
        self.word = None
        self.prev_word = None
        self.modelClass = modelClass
        self.index = 0
        self.balanced_parenthese = 0
        self.state_machine = StateMachine()
    
    def after_word(self, path: str) -> str:
        a_word = ''
        for char in path:
            if char == '/':
                break
            a_word += char
        return a_word

    def nextWord(self) -> str:
        self.sub_expression = self.sub_expression[self.index:]
        toke = ''
        chars = self.sub_expression
        for char in chars:
            if char == '/':
                break
            toke += char
        if toke != '':
            self.prev_word = self.word
            self.word = toke
            self.index = self.sub_expression.index(toke) + len(toke) + 1
        else:
            self.prev_word = self.word
            self.word = None
        return self.word

    def word_is_url(self, a_word: str) -> bool:
        return a_word.lower() == 'http:' or a_word.lower() == 'https:' or a_word.lower() == 'www.'

    def word_is_not_url(self,a_word: str) -> bool:
        return not self.word_is_url(a_word)

    def word_is_attribute(self, tk: str) -> bool:
        return self.modelClass.has_attribute(tk)
    
    def word_is_relational_operator(self, tk: str) -> bool:
        return tk in dict_relational_operator
    
    def word_is_null_operator(self, tk: str) -> bool:
        return tk in dict_null_operator

    def word_is_operation(self, tk: str) -> bool:
        if tk is None or tk.strip() == "":
            return False
        try:
            return callable(getattr(self.modelClass, tk))
        except AttributeError:
            return False

    def operation_params_count(self, tk: str):
        return len(list(getattr(self.modelClass, tk).__annotations__.keys())) -1

    def operation_params_types(self, tk: str):
        return [param[1] for param in getattr(self.modelClass, tk).__annotations__.items()][:-1]

    def get_operation_params_vals_and_types(self, tk: str):
        # todo: need to support values referenced by URLs
        params_and_types = []
        oper_params_count = self.operation_params_count(tk)
        oper_params_types = self.operation_params_types(tk)
        sql_equivalent_types = []
        for _type in oper_params_types:
            sql_equivalent_types.append(python_to_sqlalchemy_type(_type))
        params_vals = self.sub_expression.split("/")[1:oper_params_count + 1]

        for idx, val in enumerate(params_vals):
            params_and_types.append( (val, sql_equivalent_types[idx]) )

        return params_and_types

    def get_operation_query(self, tk: str):

        converted_vals = []
        oper_params_vals_and_types = self.get_operation_params_vals_and_types(tk)
        for _val, _type in oper_params_vals_and_types:
            converted_vals.append(convert_data(_val, _type))

        query = Session().query(self.modelClass).filter(getattr(self.modelClass, tk)(*converted_vals))
        whereclause = str(query).split("WHERE")[1]

        attr_full_ref = list(self.modelClass.metadata.tables.items())[0][0] + "." + self.prev_word
        whereclause = whereclause.replace(attr_full_ref, self.prev_word)
        for conv_val in converted_vals:
            whereclause = re.sub(r':[A-Za-z_0-9]+', conv_val, whereclause, count=1)

        oper_params_vals = [op[0] for op in oper_params_vals_and_types]
        operation_snippet = tk + "/" + "/".join(oper_params_vals) + "/"
        self.index = self.sub_expression.index(operation_snippet) + len(operation_snippet)
        return " ( " + whereclause.strip() + " ) "

    def word_is_logical_operator(self, tk: str) -> bool:
        return tk in dict_logical_operator

    def word_is_in_operator(self, tk: str) -> bool:
        return tk in dict_in_operator

    def word_is_parentheses(self, tk: str) -> bool:
        return tk in dict_parentheses_word

    def get_token_category(self, token):
        if self.word_is_attribute(token):
            return ATTRIBUTE_CATEGORY
        elif self.word_is_relational_operator(token):
            return RELATIONAL_OPERATOR_CATEGORY
        elif self.word_is_in_operator(token):
            return IN_OPERATOR
        elif token == AND_CATEGORY:
            return AND_CATEGORY
        elif token == OR_CATEGORY:
            return OR_CATEGORY
        elif token == BETWEEN_CATEGORY:
            return BETWEEN_CATEGORY
        elif token == PAREN_OPEN:
            return PAREN_OPEN
        elif token == PAREN_CLOSE:
            return PAREN_CLOSE
        elif self.word_is_operation(token):
            return OPERATION_CATEGORY
        else:
            return VALUE_CATEGORY

    async def convert_value(self, token):
        # value can appear in states: 3, 5, 10, 14 and 16
        url_arr = self.expression[:self.expression.index(self.sub_expression)].split("/")
        url_arr = [snippet for snippet in url_arr if snippet != ""]

        if url_arr[0] == PAREN_OPEN:
            attribute = url_arr[1]
        else:
            attribute = url_arr[0]
        # if self.state_machine.current_state in [3, 5]:
        #     attribute = url_arr[-2]
        # elif self.state_machine.current_state in [10, 16]:
        #     attribute = url_arr[-3]
        # # elif self.state_machine.current_state in [14]:
        # else:
        #     attribute = url_arr[-7]

        tuple_attrib_column_type = self.modelClass.attribute_column_type(attribute)

        if self.word_is_url(token):
            token = self.url_word()
            req = await get_request(token)
            if req.status_code == 200:
                token = req.json()
            else:
                raise IOError(f"Error in request: {token}")

        if self.prev_word in [IN_OPERATOR]:
            converted_list = []
            for value in token.split(","):
                converted_list.append(convert_data(value, tuple_attrib_column_type[-1]))
            return "(" + ",".join(converted_list) + ")"

        return convert_data(token, tuple_attrib_column_type[-1])

    async def translate_for_attribute(self, translated: str) -> str:
        tuple_attrib_column_type = self.modelClass.attribute_column_type(self.word)
        translated += tuple_attrib_column_type[1]
        # tk = self.nextWord() #After attribute word, next word could be relational operator or In operator or null operator or function operator
        # if self.word_is_relational_operator(tk):
        #     translated = await self.translate_for_relational_operator(tuple_attrib_column_type[0], tuple_attrib_column_type[2], translated) #dict_relational_operator[tk]
        # elif self.word_is_in_operator(tk):
        #     translated = await self.translate_for_in_operator(tuple_attrib_column_type[0], tuple_attrib_column_type[2], translated)
        # elif self.word_is_null_operator(tk):
        #     translated += dict_null_operator[tk]
        # elif self.word_is_operation(tk):
        #     pass
        # else:
        #     raise SyntaxError("Sintaxe error in URL")
        return translated    
    
    def translate_for_logical_operator(self, translated: str) -> str:
        translated += dict_logical_operator[self.word]
        return translated

    def url_word(self) -> str:
        a_word = ''
        balanced_paranth = 0
        for char in self.prev_word + self.sub_expression:
            if char == '(':
                balanced_paranth -= 1
            elif char == ')':
                balanced_paranth += 1
            else:
                a_word += char
            if balanced_paranth == 0:
                break
        if balanced_paranth != 0:
            res = 'Left parentheses is not balanced' if balanced_paranth < 0 else 'Right parentheses is not balanced'
            raise SyntaxError(res)
        self.index = self.sub_expression.index(a_word) + len(a_word)# + 2
        return a_word #a_word[1:]

    def sub_path_has_url(self, a_word: str) -> str:
        a_path = self.after_word(self.sub_expression[2:])  # a_path => (/http   ...
        return a_word == '(' and self.word_is_url(a_path)

    # attribute_name: str, attribute_type: str,
    async def translate_for_in_operator(self, translated: str) -> str:
        translated += dict_in_operator[self.word]
        # tk = self.nextWord()
        # if self.sub_path_has_url(tk):
        #     a_url = self.url_word()
        #     req = await get_request(a_url)
        #     if req.status_code == 200:
        #
        #         a_value = req.json()
        #         translated += convert_data(a_value, attribute_type) + " "
        #     else:
        #         raise IOError(f"Error in request: {a_url}")
        # else:
        #     enum_value = convert_data_in_enum(tk, attribute_type)
        #     translated += f"({enum_value})"
        return translated

    async def translate_for_relational_operator(self, attribute_name: str, attribute_type: str, translated: str) -> str:
        translated += dict_relational_operator[self.word] #prev word could be an attribute or function
        # tk = self.nextWord() #after relational operator a value could be: a url or value.
        # if self.sub_path_has_url(tk):
        #     a_url = self.url_word()
        #     req = await get_request(a_url)
        #     if req.status_code == 200:
        #         a_value = req.json()
        #         translated += convert_data(a_value, attribute_type)
        #     else:
        #         raise IOError(f"Error in request: {a_url}")
        # else:
        #     translated += convert_data(tk, attribute_type)
        return translated

    def translate_url_as_word(self)-> str:
        pass

    def translate_for_parantheses_word(self, translated: str) -> str:
        if self.word_is_url(self.after_word(self.sub_expression)):
            translated += self.translate_url_as_word()
        else:
            translated += dict_parentheses_word[self.word]
        return translated

    async def translate(self) -> str:
        # getattr(self.modelClass, "somar_ano").__annotations__
        translated = ''
        tk = '' #first state
        while(tk is not None):
            tk = self.nextWord()
            token_category = self.get_token_category(tk)

            try:
                self.state_machine.set_next_state(tk, token_category)
            except ValueError:
                if self.state_machine.is_final_state():
                    return translated
                else:
                    raise SyntaxError("Sintaxe error in URL")

            if token_category == ATTRIBUTE_CATEGORY:
                translated = await self.translate_for_attribute(translated)
            elif token_category in [OR_CATEGORY, AND_CATEGORY]: # todo: not supporting NAND nor NOR
                translated = self.translate_for_logical_operator(translated)
            elif token_category in [PAREN_OPEN, PAREN_CLOSE]:
                translated = self.translate_for_parantheses_word(translated)
            elif token_category == RELATIONAL_OPERATOR_CATEGORY:
                translated += dict_relational_operator[self.word]
            elif token_category in [IN_OPERATOR]:
                translated = await self.translate_for_in_operator(translated)
            elif self.word_is_operation(tk):
                translated = self.get_operation_query(tk)
            elif token_category == VALUE_CATEGORY:
                translated += await self.convert_value(tk)

            # if self.word_is_attribute(tk):
            #   translated = await self.translate_for_attribute(translated)
            # elif self.word_is_logical_operator(tk):
            #     translated = self.translate_for_logical_operator(translated)
            # elif self.word_is_parentheses(tk):
            #     translated = self.translate_for_parantheses_word(translated)

        return translated

