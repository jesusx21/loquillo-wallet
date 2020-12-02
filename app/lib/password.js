const Crypto = require('crypto');

class Password {
  encode(password) {
    const salt = Crypto.randomBytes(32).toString('hex');
    const hash = this._hashPassword(password, salt);

    return { salt, hash };
  }

  _hashPassword(password, salt) {
    const key = `${password}${salt}`;

    return Crypto.createHash('sha512')
      .update(key)
      .digest('hex');
  }
}