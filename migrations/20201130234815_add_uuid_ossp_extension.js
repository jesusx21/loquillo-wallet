exports.up = function(knex) {
  return knex.raw('CREATE EXTENSION "uuid-ossp"');
};

exports.down = function(knex) {
  return knex.raw('DROP EXTENSION "uuid-ossp"');
};
