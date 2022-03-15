from typing import Dict

from src.hyper_resource.common_resource import CONTENT_TYPE_JSON, CONTENT_TYPE_XML, CONTENT_TYPE_FLATBUFFERS
from src.orm.action_type import ActionFunction, ParamAction
representations = [CONTENT_TYPE_JSON, CONTENT_TYPE_XML, CONTENT_TYPE_FLATBUFFERS]

dic_abstract_resource_action: Dict[str, ActionFunction] = {

    'projection': ActionFunction('projection',
                                 'projection',
                               'AbstractResource',
                               [ParamAction('attribute_names', 'Enumeration')],
                               'Returns a resource, given attributes names separated by comma.',
                               'http://a-server/apis/countries/BRA/name,population',
                               representations),
}