const RootPath = require('app-root-path');

const schema = require('./schema');
const { Password } = require(`${RootPath}/app/lib`);
const { buildUserEntity } = require(`${RootPath}/domain/entities`);
const { validateSchema } = require(`${RootPath}/utils`)

class CreateUser {
  constructor(userData, database) {
    this._userData = userData;
    this._database = database;
    this._password = new Password();
  }

  async execute() {
    try {
      await this._validateData();
      const user = await this.buildUser();

      return this._saveUser(user);
    } catch (error) {
      throw error
    }
  }

  async _validateData() {
    await validateSchema(schema, this._userData);
  }

  async buildUser() {
    const passsword = this._password.encode(passsword);
    const user = await buildUserEntity({
      name: this._userData.name,
      email: this._userData.email
    });

    user.setPassword(passsword);

    return user;
  }

  saveUser(user) {
    return this._database.users.create(user);
  }
}

module.exports = CreateUser;
