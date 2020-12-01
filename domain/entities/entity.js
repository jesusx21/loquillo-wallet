const RootPath = require('app-root-path');

const { EntityDataInvalid, EntityError } = require('./errors');
const { validateSchema } = require(`${RootPath}/utils`);

class Entity {
  constructor(schema, data) {
    this._entityName = null;
    this._schema = schema;

    this.setData(data);
  }

  isNew() {
    return Boolean(this.id)
  }

  async setData(data) {
    try {
      await validateSchema(this._schema, data)
    } catch (error) {
      if (error.name === 'VALIDATION_ERROR') {
        throw new EntityDataInvalid(error, data, this._entityName);
      }

      throw new EntityError(error, this._entityName)
    }

    return Object.assign(this, data);
  }

  toJSON() {
    return Object.assign({}, this);
  }
}

module.exports = Entity;
