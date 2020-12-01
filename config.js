const knexfile = require('./knexfile');

function buildConfig() {
  const env = process.env.NODE_ENV;
  const databaseData = knexfile[env];

  return {
    database: {
      driver: databaseData.client,
      name: databaseData.connection.database
    }
  };
}

module.exports = buildConfig();
