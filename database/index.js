const UserStore = require('./stores/user');

function buildDatabase(connection, entityBuilder) {
  return {
    users: new UserStore(connection, entityBuilder.buildUserEntity)
  };
}

module.exports = buildDatabase;
