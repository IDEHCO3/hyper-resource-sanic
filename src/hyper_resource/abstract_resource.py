import json

from sanic import  response
from typing import List, Dict

from src.hyper_resource import feature_utils

MIME_TYPE_JSONLD = "application/ld+json"
from src.hyper_resource.basic_route import *
class AbstractResource:
    MAP_MODEL_FOR_CONTEXT = {}
    model_class = None

    @classmethod
    def router_id(cls):
        return BasicRoute.router_id(cls.model_class)
    @classmethod
    def router_id_path(cls):
        return BasicRoute.router_id_path(cls.model_class)
    @classmethod
    def router_list(cls):
        return BasicRoute.router_list(cls.model_class)
    @classmethod
    def router_list_path(cls):
        return BasicRoute.router_list_path(cls.model_class)

    def __init__(self, request):
        self.request = request
        self.dialect_db = None

    def dialect_DB(self):
        if self.dialect_db is None:
            self.dialect_db = self.request.app.dialect_db_class(self.request.app.db, self.metadata_table(), self.entity_class())

        return self.dialect_db

    def is_content_type_in_accept(self, accept_type: str):
        return accept_type in self.request.headers['accept']

    def protocol_host(self):
        return self.request.scheme + '://' + self.request.host

    def entity_class(self):
        raise NotImplementedError("'entity_class' must be implemented in subclasses")

    def metadata_table(self):
        return self.entity_class().__table__

    def attribute_names(self):
        return self.entity_class().all_attributes_with_dereferenceable()
        
    def fields_from_path_in_attribute_names(self, fields_from_path) -> bool:
        for att_name in fields_from_path:
            if att_name not in self.attribute_names():
                return False
        return True

    def fields_from_path_not_in_attribute_names(self, fields_from_path)-> bool :
        return not self.fields_from_path_in_attribute_names(fields_from_path)

    def dict_name_operation(self) -> Dict[str, 'function']:
        return {}

    def doc_for_operation(self, operation_name: str) -> List[str]:
        dic_name_oper = self.dict_name_operation()
        if operation_name not in dic_name_oper:
            raise LookupError(f'This {operation_name} is not supported')
        operation = dic_name_oper[operation_name]
        doc_str = operation.__doc__
        return [s.strip() for s in doc_str.split('\n') if s.strip() != '']

    async def get_representation(self):
        raise NotImplementedError("'get_representation' must be implemented in subclasses")

    async def get_representation_given_path(self, id_or_key_value, a_path):
        raise NotImplementedError("'get_representation' must be implemented in subclasses")

    async def head(self):
        return response.json("Method HEAD not implemented yet.", status=501)

    async def head_given_path(self, path):
        return response.json("Method HEAD not implemented yet.", status=501)

    async def options(self, *args, **kwargs):
        return response.json("Method OPTIONS not implemented yet.", status=501)
    
    #'/string/<parameters:path>'
    async def options_given_path(self, path):
        return await response.json("Method HEAD not implemented yet.", status=501)

    async def post(self):
        return await response.json("Method POST not implemented yet.", status=501)

    async def patch(self, id):
        return await response.json("Method PATCH not implemented yet.", status=501)

    async def put(self, id):
        return await response.json("Method PUT not implemented yet.", status=501)

    async def delete(self, id):
        return await response.json("Method DELETE not implemented yet.", status=501)

    def validate_attribute_names(self, attribute_names: List[str]) -> bool:
        s1 = set(self.dialect_DB().attribute_names())
        s2 = set(attribute_names)
        set_final = s2.difference(s1)
        if len(set_final) > 0:
            raise NameError(f"The attribute list was not found: {set_final.__str__()}")
        return True

    def validate_data(self, attribute_value: dict):
        attribute_names = attribute_value.keys()
        self.validate_attribute_names(attribute_names)
    def set_html_variables(self, html_content:str)-> str:
        return feature_utils.set_html_variables(
            html_content, self.metadata_table().name,
            json.dumps(
                self.context_class(
                    self.dialect_DB(),
                    self.metadata_table(),
                    self.entity_class()
                ).get_basic_context(),
                indent=2
            )
        )