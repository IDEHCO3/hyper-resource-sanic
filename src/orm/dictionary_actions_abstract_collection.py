from src.hyper_resource.common_resource import CONTENT_TYPE_JSON, CONTENT_TYPE_XML, CONTENT_TYPE_FLATBUFFERS
from src.orm.action_type import ActionFunction, ParamAction
from .dictionary_actions_abstract_resource import dic_abstract_resource_action

representations = [CONTENT_TYPE_JSON, CONTENT_TYPE_XML]  # , CONTENT_TYPE_FLATBUFFERS

dic_abstract_collection_lookup_action: dict[str, ActionFunction] = {

    'filter': ActionFunction('filter',
                             'AbstractCollection',
                             [ParamAction('expression', str)],
                             'Returns a subset of the collection, given a expression.',
                             'http://a-server/apis/states/filter/geom/within/Point(22, 34)',
                             representations),

    'collect': ActionFunction('collect',
                              'AbstractCollection',
                              [ParamAction('expression', str)],
                              'Returns a collection with some transformation given a expression.',
                              'http://a-server/apis/states/collect/geom/buffer/1.2',
                              representations),

    'offsetlimit': ActionFunction('offsetlimit',
                                  'AbstractCollection',
                                  [ParamAction('offset', int), ParamAction('limit', int)],
                                  'Returns a subset of the collection starting in offset. Limited by limit',
                                  'http://a-server/apis/states/offsetlimit/10&100',
                                  representations),

    'count': ActionFunction('count',
                            'AbstractCollection',
                            [],
                            'Returns the amount of resources',
                            'http://a-server/apis/states/count',
                            [CONTENT_TYPE_JSON]),

    'orderby': ActionFunction('order_by',
                              'AbstractCollection',
                              [],
                              'Returns the amount of resources',
                              'http://a-server/apis/states/orderby/name',
                              representations),

    'projection_filter': ActionFunction('projection_filter',
                                        'AbstractCollection',
                                        [ParamAction('expression', str)],
                                        'Returns a subset of the collection, given a expression.',
                                        'http://a-server/apis/states/projection/name/filter/geom/within/Point(22, 34)',
                                        representations),
}
dic_abstract_collection_lookup_action = {**dic_abstract_resource_action, **dic_abstract_collection_lookup_action}

def action_name(a_key_name: str) -> str:
    return dic_abstract_collection_lookup_action[a_key_name].name