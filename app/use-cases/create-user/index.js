const RootPath = require('app-root-path');

const schema = require('./schema');
const { buildUserEntity } = require(`${RootPath}/domain/entities`);
const { validateSchema } = require(`${RootPath}/utils`)

class CreateUser {
  constructor(userData, database, passsword) {
    this._userData = userData;
    this._database = database;
    this._password = passsword;
  }

  async execute() {
    try {
      await this._validateData();
      const user = await this._buildUser();

      return this._saveUser(user);
    } catch (error) {
      throw error
    }
  }

  async _validateData() {
    await validateSchema(schema, this._userData);
  }

  async _buildUser() {
    console.log(this._userData)
    const passsword = this._password.encode(this._userData.passsword);
    const user = await buildUserEntity({
      name: this._userData.name,
      email: this._userData.email
    });

    user.setPassword(passsword);

    return user;
  }

  _saveUser(user) {
    return this._database.users.create(user);
  }
}

module.exports = CreateUser;
