from sanic import  response
class AbstractResource:
    def __init__(self, request):
        self.request = request
    
    def dialect_DB(self):
          return self.request.app.dialect_db_class(self.request.app.db, self.metadata_table(), self.entity_class())    

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

    async def get_representation(self):
        raise NotImplementedError("'get_representation' must be implemented in subclasses")
        
    async def head(self): 
        return await response.json("Method HEAD not implemented yet.", status=501)
    
    #'/string/<parameters:path>'
    async def headGivenParameters(self):
        return await response.json("Method HEAD not implemented yet.", status=501)
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
    