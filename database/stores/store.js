const camelizeObject = require('camelcase-keys');
const snakeObject = require('snakecase-keys');
const omit = require('lodash.omit');
const isEmpty = require('lodash.isempty');
const snakeCase = require('lodash.snakecase');

const { DatabaseError, EntityNotFound, InvalidInputData, InvalidId } = require('../errors');

class Store {
  constructor(connection, buildEntity) {
    this._tableName = null;
    this._storeName = null;

    this._connection = connection;
    this._buildEntity = buildEntity;
  }

  async create(data) {
    const dataToSave = this._formatInputData(omit(data, 'id'));

    let record;

    try {
      record = await this._connection(this._tableName)
      .insert(dataToSave)
      .returning('*')
      .first();
    } catch(error) {
      return this._onUnexpectedError(error, data)
    }

    return this._formatOutputData(record);
  }

  async findById(id) {
    let record;

    try {
      record = await this._connection(this._tableName)
        .where('id', id)
        .first();
    } catch(error) {
      return this._onUnexpectedError(error, id);
    }

    if (!record) return this._onNotFoundError(id)

    return this._formatOutputData(record);
  }

  async update(data) {
    const dataToSave = this._formatInputData(omit(data, ['id', 'createdAt']));

    try {
      await this._connection(this._tableName)
        .where('id', data.id)
        .update({ ...dataToSave, updated_at: new Date() });
    } catch(error) {
      return this._onUnexpectedError(error, data);
    }

    return this.findById(data.id);
  }

  async find(query) {
    const filter = this._formatInputData(query.filter);
    const orderBy = isEmpty(filter.sort) ? [{ field: 'created_at', order: 'desc'}] : filter.sort;
    const sort = this._parseSortObject(orderBy);

    const qb = this._connection(this._tableName)
      .where(filter)
      .orderBy(sort);

    if (query.limit) qb.limit(query.limit);
    if (query.skip) qb.offset(query.skip);

    let records;

    try {
      records = await qb;
    } catch(error) {
      return this._onUnexpectedError(error);
    }

    return _formatMultipleOutputData(records);
  }

  async _findOne(query) {
    const filter = this._formatInputData(query.filter);
    const orderBy = isEmpty(query.sort) ? [{ field: 'created_at', order: 'desc'}] : query.sort;
    const sort = this._parseSortObject(orderBy);

    const qb = this._connection(this._tableName)
      .where(filter)
      .orderBy(sort)
      .first();

    const result = await qb.catch(this._onUnexpectedError)

    return this._formatOutputData(result)
  }

  _parseSortObject(sort = []) {
    return sort.map((item) => {
      return {
        column: snakeCase(item.field),
        order: item.order.toUpperCase()
      };
    });
  }

  _formatInputData(data) {
    return snakeObject(data, { deep: true });
  }

  _formatOutputData(data) {
    const entityData = camelizeObject(data, { deep: true });

    return this._buildEntity(entityData);
  }

  _formatMultipleOutputData(data) {
    const promises = data.map(this._formatOutputData.bind(this));

    return Promise.all(promises);
  }

  _onUnexpectedError(error, data = {}) {
    if (error.code === '42703') throw new InvalidInputData(error, data);
    if (error.code === '22P02') {
      if (error.file === 'uuid.c') throw new InvalidId(data);
      throw new InvalidInputData(error, data);
    }

    throw new DatabaseError(error);
  }

  _onNotFoundError(id) {
    throw new EntityNotFound(id, this._storeName);
  }
}

module.exports = Store;
