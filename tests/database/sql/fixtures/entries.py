from database.tables import Entries

from . import constants


entry_fixtures = {
    'table': Entries,
    'data': [
        {
            'id': constants.SOURCE_ENTRY_ID,
            'account_id': constants.ACCOUNT_ID,
            'transaction_id': constants.TRANSACTION_ID,
            'concept': 'Groceries',
            'amount': -2500,
        },
        {
            'id': constants.TARGET_ENTRY_ID,
            'account_id': constants.ACCOUNT_ID,
            'transaction_id': constants.TRANSACTION_ID,
            'concept': 'Salary',
            'amount': 2500,
        }
    ]
}
