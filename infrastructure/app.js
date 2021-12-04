const Hapi = require('@hapi/hapi');

const loadRoutes = require('./load-routes');

function app(args) {
  const { database, password, host, port } = args;
  const server = Hapi.server({ port, host });

  loadRoutes(server, database, password);

  return server;
}

process.on('unhandledRejection', (err) => {
  console.log(err);
  process.exit(1);
});

module.exports = app;
