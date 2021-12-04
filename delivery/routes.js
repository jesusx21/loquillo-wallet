const Controllers = require('./controllers');

const routes = {
  'POST /mr-krabz/register': {
    controller: Controllers.Sessions.register
  }
};

module.exports = routes;
