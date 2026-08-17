from . import constants

from database.tables import Entries

entry_fixtures = {
    'table': Entries,
    'data': [
        {
            'id': constants.SOURCE_ENTRY_ID,
            'account_id': constants.ALBO_ACCOUNT_ID,
            'transaction_id': constants.TRANSACTION_ID,
            'concept': 'Groceries',
            'amount': -2500,
        },
        {
            'id': constants.TARGET_ENTRY_ID,
            'account_id': constants.ALBO_ACCOUNT_ID,
            'transaction_id': constants.TRANSACTION_ID,
            'concept': 'Salary',
            'amount': 2500,
        }
    ]
}
