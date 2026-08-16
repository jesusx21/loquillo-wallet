from uuid import uuid4

from . import constants
from database.tables import Accounts


account_fixtures = {
    'table': Accounts,
    'data': [
        {
            'id': constants.ACCOUNT_ID,
            'name': 'Credit Card Account',
            'type': 'detail'
        },
        {
            'id': uuid4(),
            'name': 'Credit Card Account',
            'type': 'detail'
        },
        {
            'id': uuid4(),
            'name': 'Credit Card Account',
            'type': 'detail'
        },
        {
            'id': uuid4(),
            'name': 'Credit Card Account',
            'type': 'detail'
        },
        {
            'id': uuid4(),
            'name': 'Credit Card Account',
            'type': 'detail'
        }
    ]
}
