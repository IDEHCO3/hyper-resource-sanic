from src.orm.database import DialectDatabase
from src.hyper_resource.context.context_types import SQLALCHEMY_SCHEMA_ORG_TYPES
import copy
from environs import Env

ACONTEXT_KEYWORK = "@context"
env = Env()
env.read_env()
port = env.str("PORT", "8002")
host = env.str("HOST", "127.0.0.1")

PREFIX_HYPER_RESOURCE = "hr"

CONTEXT_TEMPLATE = {
    "@context": {
        f"{PREFIX_HYPER_RESOURCE}": f"http://{host}:{port}/core",
        "schema": "http://schema.org/",
    }
}

class AbstractContext(object):
    def __init__(self, db_dialect:DialectDatabase, metadata_table, entity_class):
        self.db_dialect = db_dialect
        self.metadata_table = metadata_table
        self.entity_class = entity_class

    def get_basic_context(self):
        context = copy.deepcopy(CONTEXT_TEMPLATE)
        context[ACONTEXT_KEYWORK].update(self.get_properties_term_definition_dict())
        return context

    def get_properties_term_definition_dict(self):
        term_definition_dict = {}
        for column in self.metadata_table.columns:
            term_definition_dict[str(column.name)] = SQLALCHEMY_SCHEMA_ORG_TYPES[type(column.type)]
        return term_definition_dict

class AbstractCollectionContext(AbstractContext):
    pass

class AbstractDetailContext(AbstractContext):
    pass