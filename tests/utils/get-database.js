const ROOT_PATH = require('app-root-path');

const { postgres } = require(`${ROOT_PATH}/database/drivers`);
const buildDatabase = require(`${ROOT_PATH}/database`);
const entities = require(`${ROOT_PATH}/domain/entities`);

module.exports = (driver = postgres) => buildDatabase(driver, entities);
