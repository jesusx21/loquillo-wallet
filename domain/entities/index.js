const User = require('./user');

function buildEntity(Entity) {
  return (data) => {
    const entity = new Entity(data)

    return entity;
  };
}

module.exports = {
  buildUserEntity: buildEntity(User)
};
