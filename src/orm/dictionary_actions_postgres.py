from numbers import Number
from typing import Dict

from src.hyper_resource.common_resource import CONTENT_TYPE_JSON
from src.orm.action_type import ActionFunction, ParamAction
representations = [CONTENT_TYPE_JSON]
dic_math_aggregate_action: Dict[str, ActionFunction] = {
    'sum': ActionFunction(name='sum',
                          name_operation='sum',
                          answer=Number,
                          param_actions=[ParamAction(name='enum_attribute',_type=str, mandatory=False, default=None, description='Name of the attributes separated by comma to group')],
                          description= 'Sum of the attribute.',
                          example="api/expenses/cost/sum",
                          representations=representations),
    'avg': ActionFunction(name='avg',
                          name_operation='avg',
                          answer=Number,
                          param_actions=[ParamAction(name='enum_attribute',_type=str, mandatory=False, default=None, description='Name of the attributes separated by comma to group')],
                          description= 'Avg of the attribute.',
                          example="api/expenses/cost/avg",
                          representations=representations),
    'max': ActionFunction(name='max',
                          name_operation='max',
                          answer=Number,
                          param_actions=[ParamAction(name='enum_attribute',_type=str, mandatory=False, default=None, description='Name of the attributes separated by comma to group')],
                          description= 'Max of the attribute.',
                          example="api/expenses/cost/max",
                          representations=representations),
    'min': ActionFunction(name='min',
                          name_operation='min',
                          answer=Number,
                          param_actions=[ParamAction(name='enum_attribute',_type=str, mandatory=False, default=None, description='Name of the attributes separated by comma to group')],
                          description= 'Max of the attribute.',
                          example="api/expenses/cost/min",
                          representations=representations),

}
dic_date_action:  Dict[str, ActionFunction] = {
    'year': ActionFunction(name='year',
                          name_operation='extract',
                          answer=Number,
                          param_actions=[],
                          description= 'Return the year of the date.',
                          example="api/expenses/date/year",
                          representations=representations),

}