const RootPath = require('app-root-path');
const isPlainObject = require('lodash.isplainobject');
const snakeCase = require('lodash.snakecase');
const clone = require('lodash.clonedeep');

const { postgres } = require(`${RootPath}/database/drivers`)
const COLLECTIONS = require('./config/collections');

function loadFixtures(fixturesData) {
  const execute = async () => {
    const fixtures = clone({ ...fixturesData });

    for (const storeName of Object.keys(fixtures)) {
      await insertIntoDatabase(storeName, fixtures[storeName]);
    }
  };

  const insertIntoDatabase = (storeName, fixtures) => {
    const tableName = COLLECTIONS[storeName];

    return postgres(tableName)
      .insert(fixtures.map(formatFixtures));
  };

  const formatFixtures = (fixtures) => {
    const data = {};

    Object.keys(fixtures).forEach((key) => {
      let value = fixtures[key];

      if (isPlainObject(value)) {
        value = formatFixtures(value);
      }

      data[snakeCase(key)] = value;
    });

    return data;
  };

  return execute();
}

module.exports = loadFixtures;
