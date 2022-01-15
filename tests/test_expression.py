#(hyper-resource-sanic-JWRMp1xC-py3.7) C:\desenv\python-des\hyper-resource-sanic\tests>pytest -q test_filter_expression.py

from typing import Dict, Tuple, Sequence, List
import unittest

from src.url_interpreter.interpreter_new import Expression


class TestExpression():

    def test_has_not_delimiter(self):
        expr = Expression("/id/gt/5/and/id/lte/101")
        assert expr.has_not_delimiter()
        expr = Expression("/sigla/in/'rj','es','go'/and/geom/within/Point(1,2)")
        assert expr.has_not_delimiter()


    def test_has_delimiter(self):
        expr = Expression("/id/gt/5/and/id/lte/101")
        assert not expr.has_delimiter()
        expr = Expression("geom/buffer/1.2/bbcontains/(/http://127.0.0.1/bc250/hidreletricas/1/)/and/")
        assert expr.has_delimiter()


    def test_delimiter_is_balanced(self):
        expr = Expression("geom/buffer/1.2/bbcontains/(/http://127.0.0.1/bc250/hidreletricas/1/)/and/")
        assert expr.is_balanced()

    def test_words(self):
        s1 = "geom/buffer/1.2/bbcontains/Point(1,2)/"
        expr = Expression(s1)
        words = expr.words()
        assert len(words) == 5
        assert words[0] == 'geom' and words[1] == 'buffer' and words[2] == '1.2'
        assert words[3] == 'bbcontains' and words[4] == 'Point(1,2)'
        twords = expr.twords()
        assert twords[0].is_simple() and twords[1].is_simple() and twords[2].is_simple()
        assert twords[3].is_simple() and twords[4].is_simple()

        s1 = "geom/buffer/1.2/bbcontains/Point(1,2)"
        expr = Expression(s1)
        words = expr.words()
        assert len(words) == 5
        assert words[0] == 'geom' and words[1] == 'buffer' and words[2] == '1.2'
        assert words[3] == 'bbcontains' and words[4] == 'Point(1,2)'
        twords = expr.twords()
        assert twords[0].is_simple() and twords[1].is_simple() and twords[2].is_simple()
        assert twords[3].is_simple() and twords[4].is_simple()

        expr = Expression("geom/buffer/1.2/bbcontains/(/http://127.0.0.1/bc250/hidreletricas/1/)/or/geom/within/(/http://127.0.0.1/bc250/ufs/RJ/)/")
        words = expr.words()
        assert words[0] == 'geom' and words[1] == 'buffer' and words[2] == '1.2'
        assert words[3] == 'bbcontains' and words[4] == 'http://127.0.0.1/bc250/hidreletricas/1'
        assert words[5] == 'or' and words[6] == 'geom' and words[7] == 'within'
        assert words[8] == 'http://127.0.0.1/bc250/ufs/RJ'
        twords = expr.twords()
        assert twords[0].is_simple() and twords[1].is_simple() and twords[2].is_simple()
        assert twords[3].is_simple() and twords[4].is_url() and twords[5].is_simple()
        assert twords[6].is_simple() and twords[7].is_simple() and twords[8].is_url()

        expr = Expression("geom/buffer/1.2/bbcontains/geom2/and/(/geom/within/geom3/or/geom/eq/geom4/)/")
        words = expr.words()
        assert words[0] == 'geom' and words[1] == 'buffer' and words[2] == '1.2'
        assert words[3] == 'bbcontains' and words[4] == 'geom2' and words[5] == 'and'
        assert words[6] == '(' and words[7] == 'geom' and words[8] == 'within' and words[9] == 'geom3'
        assert words[10] == 'or' and words[11] == 'geom' and words[12] == 'eq' and words[13] == 'geom4'
        assert words[14] == ')'
        twords = expr.twords()
        assert twords[0].is_simple() and twords[1].is_simple() and twords[2].is_simple()
        assert twords[3].is_simple() and twords[4].is_simple() and twords[5].is_simple()
        assert twords[6].is_simple() and twords[7].is_simple() and twords[8].is_simple()
        assert twords[9].is_simple() and twords[10].is_simple() and twords[11].is_simple()
        assert twords[12].is_simple() and twords[13].is_simple() and twords[14].is_simple()

        expr = Expression("/geom/buffer/1.2/bbcontains/geom2/and/(/geom/within/Polygon(-180, 180, -90, 90)/or/geom/eq/geom4/)/")
        words = expr.words()
        assert words[0] == 'geom' and words[1] == 'buffer' and words[2] == '1.2'
        assert words[3] == 'bbcontains' and words[4] == 'geom2' and words[5] == 'and' and words[6] == '('
        assert words[7] == 'geom' and words[8] == 'within' and words[9] == 'Polygon(-180, 180, -90, 90)'
        assert words[10] == 'or' and words[11] == 'geom' and words[12] == 'eq' and words[13] == 'geom4'
        twords = expr.twords()
        assert twords[0].is_simple() and twords[1].is_simple() and twords[2].is_simple()
        assert twords[3].is_simple() and twords[4].is_simple() and twords[5].is_simple()
        assert twords[6].is_simple() and twords[7].is_simple() and twords[8].is_simple()
        assert twords[9].is_simple() and twords[10].is_simple() and twords[11].is_simple()
        assert twords[12].is_simple() and twords[13].is_simple()

        expr = Expression("/(/id_objeto/gt/5/and/id_objeto/lte/56407/)/or/(/id_objeto/eq/56406/and/sigla/eq/RJ/)/")
        words = expr.words()
        assert words[0] == '(' and words[1] =='id_objeto' and words[2] == 'gt'
        assert words[3] == '5' and words[4] == 'and' and words[5] == 'id_objeto'
        assert words[6] == 'lte' and words[7] == '56407' and words[8] == ')' and words[9] == 'or'
        assert words[10] == '(' and words[11] == 'id_objeto' and words[12] == 'eq' and words[13] == '56406'
        assert words[14] == 'and' and words[15] == 'sigla' and words[16] == 'eq' and words[17] == 'RJ'
        assert words[18] == ')'
        twords = expr.twords()
        assert twords[0].is_simple() and twords[1].is_simple() and twords[2].is_simple()
        assert twords[3].is_simple() and twords[4].is_simple() and twords[5].is_simple()
        assert twords[6].is_simple() and twords[7].is_simple() and twords[8].is_simple()
        assert twords[9].is_simple() and twords[10].is_simple() and twords[11].is_simple()
        assert twords[12].is_simple() and twords[13].is_simple() and twords[14].is_simple()
        assert twords[15].is_simple() and twords[16].is_simple() and twords[17].is_simple()
        assert twords[18].is_simple()

    def test_is_balanced(self):
        expr = Expression("/(/id_objeto/gt/5/and/id_objeto/lte/56407/)/or/(/id_objeto/eq/56406/and/sigla/eq/RJ/)/")
        assert expr.is_balanced()
