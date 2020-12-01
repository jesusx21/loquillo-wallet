const { ValidationError } = require('./errors');

async function validateSchema(schema, data) {
  try {
    await schema.validateAsync(data);
  } catch(error) {
    throw new ValidationError(error);
  }
}

module.exports = validateSchema;
