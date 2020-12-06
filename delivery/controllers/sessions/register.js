const RootPath = require('app-root-path');

const { CreateUser } = require(`${RootPath}/app/use-cases`);

async function register(req, res) {
  const { payload, database, password } = req;
  const createUser = new CreateUser(payload, database, password);

  let user;

  try {
    user = await createUser.execute();
  } catch (error) {
    const response = {
      error,
      code: 'UNEXPECTED_ERROR'
    };

    let statusCode = 500

    if (error.name === 'VALIDATION_ERROR') {
      response.code = 'INVALID_DATA';
      statusCode = 400;
    }

    return res.payload(response).statusCode(statusCode);
  }

  return res.payload(user).statusCode(201);
}

module.exports = register;
