from . import constants

from database.tables import Accounts


account_fixtures = {
    'table': Accounts,
    'data': [
        {
            'id': constants.ALBO_ACCOUNT_ID,
            'name': 'Albo Account',
            'type': 'detail'
        },
        {
            'id': constants.BBVA_ACCOUNT_ID,
            'name': 'BBVA Account',
            'type': 'detail'
        },
        {
            'id': constants.NU_BANK_ACCOUNT_ID,
            'name': 'Nu Bank Account',
            'type': 'detail'
        },
        {
            'id': constants.STORI_ACCOUNT_ID,
            'name': 'Stori Account',
            'type': 'detail'
        },
        {
            'id': constants.HSBC_ACCOUNT_ID,
            'name': 'HSBC Account',
            'type': 'detail'
        }
    ]
}
