const { OBJECT, UUID, STRING, EMAIL } = require('../types');

const USER_SCHEMA = OBJECT({
  id: UUID,
  name: STRING({ allowEmpty: false }),
  email: EMAIL,
  password: OBJECT({
    salt: STRING({ allowEmpty: false }),
    hash: STRING({ allowEmpty: false })
  }, ['salt', 'hash'])
},['id', 'name', 'email', 'password']);

module.exports = USER_SCHEMA
