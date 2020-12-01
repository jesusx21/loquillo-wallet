const config = require('./infrastructure/config');
const buildApp = require('./infrastructure/app')
const buildDatabase = require('./database');
const drivers = require('./database/drivers');
const entitiesBuilder = require('./domain/entities');

async function initializeServer() {
  const db = drivers[config.database.driver];
  const database = buildDatabase(db, entitiesBuilder);

  const app = buildApp({
    database,
    port: config.server.port,
    host: config.server.host
  });

  await app.start()
    .then(() => {
      console.log(`
        ||\\\\            //||      ||=======||                                 ||    //        ||=======||            ||===||        ||=======||      ============
        ||  \\\\        //  ||      ||        ||                                ||  //          ||        ||          ||     ||       ||        ||               //
        ||    \\\\    //    ||      ||        ||                                ||//            ||        ||         ||       ||      ||        ||             //
        ||      \\\\//      ||      ||=======||                                 ||\\\\            ||=======||          ||=======||      ||=======||            //
        ||                ||      ||         \\\\                               ||  \\\\          ||       \\\\          ||       ||      ||        ||         //
        ||                ||      ||           \\\\     ||==||                  ||    \\\\        ||         \\\\        ||       ||      ||        ||       //
        ||                ||      ||             \\\\   ||==||                  ||      \\\\      ||           \\\\      ||       ||      ||=======||      ============
      `);

      console.log('Server runing on %s', app.info.uri);
    });
}

initializeServer();