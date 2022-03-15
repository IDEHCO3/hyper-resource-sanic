from typing import Dict

from src.hyper_resource.common_resource import CONTENT_TYPE_JSON, CONTENT_TYPE_XML, CONTENT_TYPE_FLATBUFFERS
from src.orm.action_type import ActionFunction, ParamAction
from .dictionary_actions_abstract_resource import dic_abstract_resource_action

representations = [CONTENT_TYPE_JSON, CONTENT_TYPE_XML]  # , CONTENT_TYPE_FLATBUFFERS

dic_abstract_collection_lookup_action: Dict[str, ActionFunction] = {

    'filter': ActionFunction('filter',
                             'filter',
                             'AbstractCollection',
                             [ParamAction('expression', str)],
                             'Returns a subset of the collection, given a expression.',
                             'http://a-server/apis/states/filter/geom/within/Point(22, 34)',
                             representations),

    'collect': ActionFunction('collect',
                              'collect',
                              'AbstractCollection',
                              [ParamAction('enum_attribute_names', str), ParamAction('attribute_name', str)],
                              'Returns a collection with some transformation given a expression.',
                              'http://a-server/apis/states/collect/name,area&geom/buffer/1.2',
                              representations),

    'projection': ActionFunction('projection',
                                 'projection',
                                  'AbstractCollection',
                                  [ParamAction('enum_attribute_names', str)],
                                  'Returns a collection with attribute names',
                                  'http://a-server/apis/states/projetion/name,area',
                                  representations),

    'distinct': ActionFunction('distinct',
                               'distinct',
                               'AbstractCollection',
                               [ParamAction('enum_attribute_names', str)],
                               'Returns a collection with distinct values in attribute names',
                               'http://a-server/apis/states/distinct/name,area',
                                  representations),

    'offsetlimit': ActionFunction('offsetlimit',
                                  'offsetlimit',
                                  'AbstractCollection',
                                  [ParamAction('offset', int), ParamAction('limit', int)],
                                  'Returns a subset of the collection starting in offset. Limited by limit',
                                  'http://a-server/apis/states/offsetlimit/10&100',
                                  representations),

    'count': ActionFunction('count',
                            'count',
                            'AbstractCollection',
                            [],
                            'Returns the amount of resources',
                            'http://a-server/apis/states/count',
                            [CONTENT_TYPE_JSON]),
    'sum': ActionFunction('sum',
                            'sum',
                            'AbstractCollection',
                            [ParamAction('attribute_name', str)],
                            'Returns the sum of given attribute in resources.The attribute must be a number.',
                            'http://a-server/apis/states/sum/salary',
                            [CONTENT_TYPE_JSON]),
    'avg': ActionFunction('avg',
                            'avg',
                            'AbstractCollection',
                            [ParamAction('attribute', str)],
                            'Returns the means of given attribute in resources.The attribute must be a number.',
                            'http://a-server/apis/states/avg/salary',
                            [CONTENT_TYPE_JSON]),
    'group-by-count': ActionFunction('group-by-count',
                                     'group_by_count',
                                  'AbstractCollection',
                                  [ParamAction('enum_attribute', str), ParamAction('attribute_name', int)],
                                  'Returns a subset of the collection starting in offset. Limited by limit',
                                  'http://a-server/apis/states/offsetlimit/10&100',
                                  representations),
    'orderby': ActionFunction('orderby',
                              'order_by',
                              'AbstractCollection',
                              [],
                              'Returns the amount of resources',
                              'http://a-server/apis/states/orderby/name',
                              representations),
    'groupby': ActionFunction('groupby',
                              'group_by',
                              'AbstractCollection',
                              [ParamAction('enum_attribute', str)],
                              'Returns resources grouped by',
                              'http://a-server/apis/states/groupby/region',
                              representations),

    'projection-filter': ActionFunction('projection-filter',
                                        'projection_filter',
                                        'AbstractCollection',
                                        [ParamAction('expression', str)],
                                        'Returns a subset of the collection, given a expression.',
                                        'http://a-server/apis/states/projection/name/filter/geom/within/Point(22, 34)',
                                        representations),
}
dic_abstract_collection_lookup_action = {**dic_abstract_resource_action, **dic_abstract_collection_lookup_action}

def action_name(a_key_name: str) -> str:
    return dic_abstract_collection_lookup_action[a_key_name].name