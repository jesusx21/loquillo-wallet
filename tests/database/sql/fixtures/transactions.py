from uuid import uuid4

from . import constants

from database.tables import Transactions

transaction_fixtures = {
    'table': Transactions,
    'data': [
        {
            'id': constants.TRANSACTION_ID,
            'status': 'completed'
        },
        {
            'id': uuid4(),
            'status': 'pending'
        },
        {
            'id': uuid4(),
            'status': 'failed'
        }
    ]
}
