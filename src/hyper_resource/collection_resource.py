import time
from asyncpg import UniqueViolationError, DataError
import sanic
from typing import Dict, List, Optional
from src.hyper_resource.abstract_resource import AbstractResource, MIME_TYPE_JSONLD
from src.hyper_resource.context.abstract_context import AbstractCollectionContext
from src.hyper_resource.common_resource import CONTENT_TYPE_HTML, CONTENT_TYPE_JSON, CONTENT_TYPE_XML, dict_to_xml
from .abstract_collection_resource import AbstractCollectionResource
from ..orm.query_builder import QueryBuilder
from ..url_interpreter.interpreter_error import PathError
from ..url_interpreter.interpreter_new import InterpreterNew
from ..orm.dictionary_actions_abstract_collection import dic_abstract_collection_action, action_name

class CollectionResource(AbstractCollectionResource):
    def __init__(self, request):
        super().__init__(request)
        self.context_class = AbstractCollectionContext
        self.function_names = None

    def get_function_names(self) -> List[str]:
        if self.function_names is None:
            self.function_names = list(dic_abstract_collection_action.keys())
        return self.function_names

    async def get_representation_given_path(self, path: str) -> str:
        try:
            paths: List[str] = self.normalize_path_as_list(path, '/*/')
            qb: QueryBuilder = QueryBuilder(dialect_db=self.dialect_DB(), entity_class=self.entity_class(), prefix_column=self.protocol_host())
            qb.has_geometry = False
            for path in paths:
                await self.execute_qb_function(qb, path)
            qb.add_table_name(self.dialect_DB().schema_table_name())
            return await self.response_by_qb(qb)
        except PathError as err:
            return sanic.response.json(err.message, err.code)
        except (RuntimeError, TypeError, NameError) as err:
            return sanic.response.json("Error {0}". format(err))

