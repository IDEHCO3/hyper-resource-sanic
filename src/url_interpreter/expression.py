import re
# from re import Match
from typing import List, Optional

from re import Match

from src.orm.database import DialectDatabase
from src.orm.models import AlchemyBase
from src.url_interpreter.interpreter_error import PathError
from src.url_interpreter.tword import TWord


LEFT_DELIMITER = r'\/\(\/'
RIGHT_DELIMITER = r'\/\)\/'
REGEX_DELIMITER = r'(\/\(\/.*?\/\)\/)'
TEMP_WORD = 'word-54f7a73c-ff96-479b-b9a8-72e7b730d2cc'

class Expression:
    def __init__(self, string: str = None):
        self.string: str = string
        self._matches: Optional[List[Match]] = None
        self._twords: Optional[List[TWord]] = None

    def matches(self) -> List[Match]:
        if self._matches is None:
            pattern = re.compile(r'(/\(/)|(/\)/)', re.UNICODE)
            self._matches = [match for match in pattern.finditer(self.string)]
        return self._matches

    def has_not_delimiter(self) -> bool:
        return not self.has_delimiter()

    def has_delimiter(self) -> bool:
        return len(self.matches()) > 1

    def is_balanced(self) -> bool:
        count_left = count_right = 0
        for m in self.matches():
            if m.group() == '/(/':
                count_left += 1
            elif m.group() == '/)/':
                count_right += 1
        return count_left == count_right

    def is_begin_delimiter_with_url(self, idx: int) -> bool:
        # print(self.string[idx + 3: idx + 3 + 5].lower())
        return self.string[idx: idx + 3] == '/(/' and \
               (self.string[idx + 3: idx + 3 + 5].lower() == 'http:' or
                self.string[idx + 3: idx + 3 + 6].lower() == 'https:' or
                self.string[idx + 3: idx + 3 + 4].lower() == 'www.')

    def is_begin_delimiter(self, idx: int) -> bool:
        size = len(self.string)
        if idx + 2 >= size:
            return False
        return self.string[idx: idx + 3] == '/(/'

    def is_end_delimiter(self, idx: int) -> bool:
        size = len(self.string)
        if idx + 2 >= size:
            return False
        return self.string[idx:idx + 3] == '/)/'

    def initialize_simple_twords(self) -> List[TWord]:
        if self._twords is None:
            str_aux = self.string
            if str_aux[0] == '/':
                str_aux = str_aux[1:]
            if str_aux[-1] == '/':
                str_aux = str_aux[0:-1]
            ls = str_aux.split('/')
            self._twords = [TWord(st, TWord.SIMPLE_CATEGORY) for st in ls]

        return self._twords

    def initialize_twords(self) -> List[TWord]:
        if not self.is_balanced():
            raise PathError("Unbalanced parentheses", 400)

        if self.has_not_delimiter():
            return self.initialize_simple_twords()

        return self.initialize_complex_twords()

    def initialize_complex_twords(self) -> List[TWord]:
        if self._twords is not None:
            return self._twords

        a_word: str = ''
        list_word: List[TWord] = []

        e = self.string
        if e[0] == '/' and not self.is_begin_delimiter(0):
            e = e[1:]
            self.string = self.string[1:]
        size_exp: int = len(e)
        i: int = 0
        while i < size_exp:
            if self.is_begin_delimiter_with_url(i):
                if i > 0:  # start with /(/
                    list_word.append(TWord(a_word, TWord.SIMPLE_CATEGORY))
                    a_word = ''
                i += 3
                while i < size_exp:
                    if self.is_end_delimiter(i):
                        list_word.append(TWord(a_word, TWord.URL_CATEGORY))
                        a_word = ''
                        i += 3
                        break
                    else:
                        a_word += e[i]
                        i += 1
            elif e[i] == '/':
                if len(a_word):
                    list_word.append(TWord(a_word, TWord.SIMPLE_CATEGORY))
                a_word = ''
                i += 1
            if i < size_exp:
                a_word += e[i]
            i += 1

        if len(a_word) > 0:
            list_word.append(TWord(a_word, TWord.COMPLEX_CATEGORY))
        self._twords = list_word
        return self._twords

    def twords(self) -> List[TWord]:
        """
        :rtype: List[TWord]
        """
        if self._twords is None:
            self._twords = self.initialize_twords()
        return self._twords

    def words(self) -> List[str]:
        list_tword = self.twords()
        return [tword.word for tword in list_tword]


class MultiExpression:

    def __init__(self, string: str, model_class: type, dialect_db: DialectDatabase):
        self.string = string
        self._expressions: List[Optional[Expression]] = []
        self.model_class: type = model_class
        self.dialect_db = dialect_db

    def get_expressions(self) -> List[Expression]:
        return self._expressions