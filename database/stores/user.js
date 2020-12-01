const Store = require('./store');

class UserStore extends Store {
  constructor(connection, buildEntity) {
    super(connection, buildEntity);

    this._tableName = 'users';
    this._storeName = 'User'
  }
}

module.exports = UserStore;
