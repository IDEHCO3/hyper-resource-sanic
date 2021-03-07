import json

from sanic import  response
from typing import List, Dict, Union

MIME_TYPE_JSONLD = "application/ld+json"

class AbstractResource:
    MAP_MODEL_FOR_CONTEXT = {}
    MAP_MODEL_FOR_ROUTE = {}

    def __init__(self, request):
        self.request = request
        self.dialect_db = None

    def dialect_DB(self):
        if self.dialect_db is None:
            self.dialect_db = self.request.app.dialect_db_class(self.request.app.db, self.metadata_table(), self.entity_class())
        return self.dialect_db

    def is_content_type_in_accept(self, accept_type: str):
        return accept_type in self.request.headers['accept']

    def entity_class(self):
        raise NotImplementedError("'entity_class' must be implemented in subclasses")

    def metadata_table(self):
        return self.entity_class().__table__

    def attribute_names(self):
        return self.entity_class().attribute_names()
        
    def fields_from_path_in_attribute_names(self, fields_from_path):
        for att_name in fields_from_path:
            if att_name not in self.attribute_names():
                return False
        return True

    def fields_from_path_not_in_attribute_names(self, fields_from_path):
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

    def remove_last_slash(self, uri:str):
        return uri[:-1] if uri.endswith("/") else uri

    def create_url_to_foreign_key(self, column_name:str, fk_id:int):
        fk_model = self.dialect_DB().get_model_by_foreign_key(self.dialect_DB().foreign_key_column_by_name(column_name))
        fk_schema_with_name = fk_model.__table__.fullname
        # WARNING: Only supports single fields primary keys
        id_field = [pk_cols.name for pk_cols in self.dialect_DB().get_model_by_foreign_key(self.dialect_DB().foreign_key_column_by_name(column_name)).__table__.primary_key.columns][0]
        related_route = self.get_related_route(fk_model)

        path = "".join(self.remove_last_slash(related_route.uri).split("/")[:-1]) + "/"
        return self.request.scheme + "://" + self.request.host + "/" + path + str(fk_id)
        # query = f'select CONCAT(\'http://teste/\', {fk_id}) from {fk_schema_with_name} where {id_field}={fk_id}'
        # record = await self.dialect_DB().db.fetch_one(query)
        # url = [v for v in record.values()][0]
        # return url

    def add_foreign_keys_references(self, data:Union[str,Dict]):
        serialized = json.loads(data) if type(data) == str else data

        fk_names = self.dialect_DB().foreign_keys_names()
        for name in fk_names:
            url = self.create_url_to_foreign_key(name, serialized[name])
            serialized[name] = url

        return json.dumps(serialized)

    def get_related_route(self, model):
        for key, _tuple in self.request.app.router.routes_names.items():
            _name, _route = _tuple
            parent_function = _route[0]
            if parent_function.__module__ == self.MAP_MODEL_FOR_ROUTE[model].__module__ and _route[2].pattern.endswith("(-?\\d+)$"):
                return _route

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
    """
        
    
    public async patch() {
        return this.response.status(501).json("Method PATCH not implemented yet.");
    }
    public async options() {
        return this.response.json(this.context.contextResource());
    }
    public async optionsGivenParameters() {
        return;
    }
    public async post(attributeNameValueJsonObject) {
        let repository = connection.getRepository(this.entity_class());
        const entity = await repository.save(attributeNameValueJsonObject);
        return this.response.status(201).json(entity[this.primaryKeyName()]);
    }
    public async delete() {
        let whereStr = `${this.primaryKeyName()} = :${this.primaryKeyName()}`;
        let whereParam = { [this.primaryKeyName()]: this.request.params["id"] };
        const res = await connection
        .createQueryBuilder()
        .delete()
        .from(this.entity_class())
        .where(whereStr, whereParam)
        .execute();
        return this.response.status(200).json(1);
    }
    public async put(attributeNameValueJsonObject) {
        let res = await connection
        .createQueryBuilder()
        .update(this.entity_class())
        .set(attributeNameValueJsonObject)
        .where(`${this.primaryKeyName()} = :${this.primaryKeyName()}`, {
            [this.primaryKeyName()]: this.request.params["id"],
        })
        .execute();
        return this.response.status(200).json(1);
    }
    """
    