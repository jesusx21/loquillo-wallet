const Joi = require('joi');

const schema = Joi.object({
  id: Joi.string()
    .guid({ version: ['uuidv4'] })
    .optional(),
  name: Joi.string()
    .optional(),
  email: Joi.string()
    .email()
    .optional()
});

module.exports = schema;
