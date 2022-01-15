from typing import Dict, Tuple, Sequence, List
import unittest
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.attributes import InstrumentedAttribute

from src.orm.database_postgis import DialectDbPostgis
from src.url_interpreter.interpreter import *
from src.models.lim_unidade_federacao_a import LimUnidadeFederacaoA
import pytest
import asyncio
class TestFeatureCollection():
    @pytest.mark.asyncio
    async def test_get_representation_given_path(self):
        url = 'http://127.0.0.1:8000/lim-unidade-federacao-a-list/bbcontains/Point(-45.66, -23.71)'

