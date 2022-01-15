from typing import List, Optional
from src.orm.converter import ConverterType
FUNCTION = 1
ATTRIBUTE = 2

#This dictionary is related to BaseGeometry and subclasses.
# The key is function or attribute name.
# The value is a tuple with a dictionary and int. The dictionary is like __annotations__.
# The int is 1 for FUNCTION or 2 for ATTRIBUTE
class ParamAction:
    def __init__(self, name: str, _type: type, mandatory: bool = True, default: object = None, description: str = None,
                 representations: Optional[List[str]] = None):
        if representations is None:
            representations = []
        self.name = name
        self._type = _type
        self.mandatory = mandatory
        self.default = default
        self.description = description
        self.representations = representations

    def arg_as_value(self, a_value: str):

        if self._type == int:
            return int(a_value)
        if self.type == float:
            return float(a_value)
        if self._type == str:
            return str(a_value)
        return a_value



class Action:
    def __init__(self, name: str,  answer: object = None, description: str = None, example: str = None, representations: List[str] =[]):
        self.name = name
        self.answer = answer
        self.description = description
        self.example = example
        self.representations = representations

    def count_params(self):
        return NotImplementedError("'count_params' must be implemented in subclasses")

    def count_mandatory_params(self):
        return NotImplementedError("'count_mandatory_params' must be implemented in subclasses")

    def execute(self, obj, action_names: List[str]) -> object:
        raise NotImplementedError("'execute' must be implemented in subclasses")

class ActionAttribute(Action):
    def __init__(self, name: str,  answer: object=None, description: str = None, example: str = None, representations: List[str] =[]):
        super().__init__(name, answer, description, example, representations)

    def count_params(self):
        return 0

    def count_mandatory_params(self):
        return 0

    async def execute(self, obj, action_names: List[str]) -> object:
        return getattr(obj, self.name)

class ActionFunction(Action):

    def __init__(self, name: str, answer: object = None, param_actions: List[ParamAction] = [], description: str = None, example: str = None, representations: List[str] =[]):
        super().__init__(name, answer, description, example, representations)
        self.param_actions = param_actions

    def count_params(self):
        return len(self.param_actions)

    def count_mandatory_params(self):
        return len([ param for param in self.param_actions if param.mandatory ])

    def has_parameters(self) -> bool:
        return len(self.param_actions) > 0

    def has_not_parameters(self) -> bool:
        return not self.has_parameters()

    def param_types(self) -> List[type]:
        return [param._type for param in self.param_actions]

    async def execute(self, obj, action_names: List[str]) -> object:
        if not self.has_parameters():
            return getattr(obj, self.name)()
        if len(action_names) == 0:
            para_text = f" these parameters: {self.param_actions}" if self.count_params() > 1 else f" this parameter: {self.param_actions}"
            raise SyntaxError(f"The operation {self.name} must have at least {para_text}")
        params = action_names.pop(0).split('&')
        if len(params) > self.count_params() or len(params) < self.count_mandatory_params():
            raise SyntaxError(f"Incorrect number of parameters in the operation {self.name}")
        paramets = await ConverterType().convert_parameters(params, self.param_types())
        result = getattr(obj, self.name)(*paramets)
        return result
