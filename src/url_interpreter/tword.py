
class TWord:
    URL_CATEGORY = 'URL'
    SIMPLE_CATEGORY = 'SIMPLE'
    COMPLEX_CATEGORY = 'COMPLEX'

    def __init__(self, word: str, category: str):
        self.word = word
        self.category = category

    def __repr__(self):
        return self.word

    def is_url(self) -> bool:
        return self.category == TWord.URL_CATEGORY

    def is_simple(self) -> bool:
        return self.category == TWord.SIMPLE_CATEGORY

    def is_complex(self):
        return self.category == TWord.COMPLEX_CATEGORY

    def __repr__(self):
        return f'{self.word}'



