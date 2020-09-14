from typing import Dict, Tuple, Sequence, List, Any
import httpx

async def get_request(url):
    async with httpx.AsyncClient() as client:
      return await client.get(url)

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
class Token:
    types = ['ATTRIBUTE', 'BEGIN_PARENTHESE']
    def __init__(self, word, type, representation):
        self.word = word
        self.type = type
        self.representation = representation


class Interpreter:
    def __init__(self, an_expression, modelClass):
        self.expression = an_expression[1:] if an_expression[0] == '/' else an_expression
        self.sub_expression = self.expression
        self.word = None
        self.prev_word = None
        self.modelClass = modelClass
        self.index = 0
        self.balanced_parenthese = 0
    
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
        return False

    def word_is_logical_operator(self, tk: str) -> bool:
        return tk in dict_logical_operator

    def word_is_in_operator(self, tk: str) -> bool:
        return tk in dict_in_operator

    def word_is_parentheses(self, tk: str) -> bool:
        return tk in dict_parentheses_word

    async def translate_for_attribute(self, translated: str) -> str:
        tuple_attrib_column_type = self.modelClass.attribute_column_type(self.word)
        translated += tuple_attrib_column_type[1]
        tk = self.nextWord() #After attribute word, next word could be relational operator or In operator or null operator or function operator
        if self.word_is_relational_operator(tk):
            translated = await self.translate_for_relational_operator(tuple_attrib_column_type[0], tuple_attrib_column_type[2], translated) #dict_relational_operator[tk]
        elif self.word_is_in_operator(tk):
            translated = await self.translate_for_in_operator(tuple_attrib_column_type[0], tuple_attrib_column_type[2], translated)
        elif self.word_is_null_operator(tk):
            translated += dict_null_operator[tk]
        elif self.word_is_operation(tk):
            pass
        else:
            raise SyntaxError("Sintaxe error in URL")
        return translated    
    
    def translate_for_logical_operator(self, translated: str) -> str:
        translated += dict_logical_operator[self.word]
        return translated

    def url_word(self) -> str:
        a_word = ''
        balanced_paranth = 0
        for char in self.sub_expression:
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
        self.index = self.sub_expression.index(a_word) + len(a_word) + 2
        return a_word[1:]

    def sub_path_has_url(self, a_word: str) -> str:
        a_path = self.after_word(self.sub_expression[2:])  # a_path => (/http   ...
        return a_word == '(' and self.word_is_url(a_path)

    async def translate_for_in_operator(self, attribute_name: str, attribute_type: str, translated: str) -> str:
        translated += dict_in_operator[self.word]
        tk = self.nextWord()
        if self.sub_path_has_url(tk):
            a_url = self.url_word()
            req = await get_request(a_url)
            if req.status_code == 200:

                a_value = req.json()
                translated += convert_data(a_value, attribute_type) + " "
            else:
                raise IOError(f"Error in request: {a_url}")
        else:
            enum_value = convert_data_in_enum(tk, attribute_type)
            translated += f"({enum_value})"
        return translated

    async def translate_for_relational_operator(self, attribute_name: str, attribute_type: str, translated: str) -> str:
        translated += dict_relational_operator[self.word] #prev word could be an attribute or function
        tk = self.nextWord() #after relational operator a value could be: a url or value.
        if self.sub_path_has_url(tk):
            a_url = self.url_word()
            req = await get_request(a_url)
            if req.status_code == 200:
                a_value = req.json()
                translated += convert_data(a_value, attribute_type)
            else:
                raise IOError(f"Error in request: {a_url}")
        else:
            translated += convert_data(tk, attribute_type)
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
        translated = ''
        tk = '' #first state
        while(tk is not None):
            tk = self.nextWord()
            if self.word_is_attribute(tk):
              translated = await self.translate_for_attribute(translated)
            elif self.word_is_logical_operator(tk):
                translated = self.translate_for_logical_operator(translated)
            elif self.word_is_parentheses(tk):
                translated = self.translate_for_parantheses_word(translated)

        return translated

