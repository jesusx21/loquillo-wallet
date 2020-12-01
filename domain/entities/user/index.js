const schema = require('./schema');
const Entity = require('../entity');

class User extends Entity {
  constructor(data) {
    super(schema, data);

    this._entityName = 'User';
  }
}

module.exports = User;
