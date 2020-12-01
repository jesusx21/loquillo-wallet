const testUtils = require(`${ROOT_PATH}/tests/utils`);

const USER_RECIPE = [{
  id: '3f54d840-6e65-4b9d-b98f-cd57bc7a524f',
  name: 'John Doe',
  email: 'jon@example.com'
}, {
  id: 'f9467cd6-9a1c-4ad2-923b-41905fd2a779',
  name: 'Jane Doe',
  email: 'jane@example.com'
}];

module.exports = {
  users: testUtils.generateFixtures('user', USER_RECIPE)
};
