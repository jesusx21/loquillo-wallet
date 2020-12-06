const config = require('./infrastructure/config');
const buildApp = require('./infrastructure/app')
const buildDatabase = require('./database');
const Password = require('./app/lib/password');
const drivers = require('./database/drivers');
const entitiesBuilder = require('./domain/entities');

async function initializeServer() {
  const db = drivers[config.database.driver];
  const database = buildDatabase(db, entitiesBuilder);
  const password = new Password();

  const app = buildApp({
    database,
    password,
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