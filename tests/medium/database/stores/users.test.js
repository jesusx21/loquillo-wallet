const uuid = require('uuid');
const { expect } = require('chai');

const fixtures = require('./fixtures');
const { buildUserEntity } = require(`${ROOT_PATH}/domain/entities`);
const testUtils = require(`${ROOT_PATH}/tests/utils`);

const USER_ID = '3f54d840-6e65-4b9d-b98f-cd57bc7a524f';

async function createUser(data, database) {
  const userEntity = await buildUserEntity(data);
  const user = await database.users.create(userEntity);

  return user.toJSON();
}

async function updateUser(data, database) {
  const userEntity = await buildUserEntity(data);
  const user = await database.users.update(userEntity);

  return user.toJSON();
}

describe('Interfaces - Database', () => {
  describe('Stores', () => {
    describe('Users Store', () => {
      let database;

      beforeEach(async () => {
        database = testUtils.getDatabase();

        await testUtils.resetDatabase();
        await testUtils.loadFixtures(fixtures);
      });

      describe('Create', () => {
        it('should return the user created', async () => {
          const data = {
            name: 'Jesus',
            email: 'jesus@gmail.com'
          };

          const user = await createUser(data, database);

          expect(user.id).to.exist;
          expect(user.name).to.be.equal(data.name);
          expect(user.email).to.be.equal(data.email);
        });

        it('should return error on invalid data', () => {
          const data = {
            name: 'Jesus',
            email: 'not an email'
          };

          return createUser(data, database)
            .then(() => Promise.reject(new Error('unexpected path')))
            .catch((error) => expect(error.name).to.be.equal('ENTITY_DATA_INVALID'));
        });

        it('should return error when data sent is not an entity', () => {
          const data = {
            name: 'Jesus',
            email: 'jesus@gmail.com'
          };

          return database.users.create(data)
            .then(() => Promise.reject(new Error('unexpected path')))
            .catch((error) => expect(error.name).to.be.equal('INPUT_IS_NOT_AN_ENTITY'));
        });
      });

      describe('Find By Id', () => {
        it('should return user by its id', async () => {
          const user = await database.users.findById(USER_ID);
          const userData = user.toJSON();

          expect(userData.id).to.be.equal(USER_ID);
          expect(userData.name).to.be.equal('John Doe');
          expect(userData.email).to.be.equal('john@example.com');
        });

        it('should return error when user was not found', () => {
          const unexistentUserId = uuid.v4();

          return database.users.findById(unexistentUserId)
            .then(() => Promise.reject(new Error('unexpected path')))
            .catch((error) => {
              expect(error.name).to.be.equal('ENTITY_NOT_FOUND');
              expect(error.message).to.be.equal(
                `User with query "{"id":"${unexistentUserId}"}" was not found`
              );
            });
        });

        it('should return error when id is invalid', () => {
          const invalidId = 'invalid-id';

          return database.users.findById(invalidId)
            .then(() => Promise.reject(new Error('unexpected path')))
            .catch((error) => {
              expect(error.name).to.be.equal('INVALID_ID');
              expect(error.message).to.be.equal(`Id "${invalidId}" is not a uuid`);
            });
        })
      });

      describe('Update', () => {
        it('should update the user', async () => {
          const data = {
            id: USER_ID,
            name: 'John Adams Dow'
          };

          const user = await updateUser(data, database);

          expect(user.id).to.exist;
          expect(user.name).to.be.equal(data.name);
          expect(user.email).to.be.equal('john@example.com');
        });

        it('should return error when input data is not an entity', async () => {
          const data = {
            id: USER_ID,
            name: 'John Adams Dow'
          };

          return database.users.update(data, database)
            .then(() => Promise.reject(new Error('unexpected path')))
            .catch((error) => expect(error.name).to.be.equal('INPUT_IS_NOT_AN_ENTITY'));
        });

        it('should return error when user does not exist', async () => {
          const data = {
            id: uuid.v4(),
            name: 'John Adams Dow'
          };

          return updateUser(data, database)
            .then(() => Promise.reject(new Error('unexpected path')))
            .catch((error) => {
              expect(error.name).to.be.equal('ENTITY_NOT_FOUND');
              expect(error.message).to.be.equal(
                `User with query "{"id":"${data.id}"}" was not found`
              );
            });
        });

        it('should return error on invalid data', async () => {
          const data = {
            id: USER_ID,
            email: 'John Adams Dow'
          };

          return updateUser(data, database)
            .then(() => Promise.reject(new Error('unexpected path')))
            .catch((error) => expect(error.name).to.be.equal('ENTITY_DATA_INVALID'));
        });
      });
    });
  });
});
