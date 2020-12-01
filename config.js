const RootPath = require('app-root-path');
const dotenv = require('dotenv');

const knexfile = require('./knexfile');

function buildConfig() {
  const env = process.env.NODE_ENV;
  const path = `${RootPath}/.env/${env}.env`;
  const { parsed: envObject } =  dotenv.config({ path });

  const databaseData = knexfile[env];

  return {
    database: {
      driver: databaseData.client,
      name: databaseData.connection.database
    },
    server: {
      host: envObject.SERVER_HOST,
      port: Number(envObject.SERVER_PORT)
    }
  };
}

module.exports = buildConfig();
