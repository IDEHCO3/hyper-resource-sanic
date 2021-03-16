from src.hyper_resource.util import  convert_camel_case_to_hifen
class BasicRoute:

    @classmethod
    def router_id(cls, model_class):
        return f'/{convert_camel_case_to_hifen(model_class.__name__)}-list/<id:int>'

    @classmethod
    def router_id_path(cls, model_class):
        return f'/{convert_camel_case_to_hifen(model_class.__name__)}-list/<id:int>/<path:path>'

    @classmethod
    def router_list(cls, model_class):
        return f'/{convert_camel_case_to_hifen(model_class.__name__)}-list'

    @classmethod
    def router_list_path(cls, model_class):
        return f'/{convert_camel_case_to_hifen(model_class.__name__)}-list/<path:path>'