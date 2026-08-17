from uuid import uuid4

from . import constants

from database.tables import Transactions

transaction_fixtures = {
    'table': Transactions,
    'data': [
        {
            'id': constants.TRANSACTION_ID,
            'description': 'Initial transaction',
            'status': 'completed'
        },
        {
            'id': uuid4(),
            'description': 'Second transaction',
            'status': 'pending'
        },
        {
            'id': uuid4(),
            'description': 'Third transaction',
            'status': 'failed'
        }
    ]
}
