from domain.entities.account import Account, AccountType
from . import constants

accounts = [
    Account(
        id=constants.BBVA_ACCOUNT_ID,
        name='BBVA Account',
        type=AccountType.DETAIL,
    ),
    Account(
        id=constants.CASH_ACCOUNT_ID,
        name='Cash Account',
        type=AccountType.DETAIL,
    ),
    Account(
        id=constants.SANTANDER_ACCOUNT_ID,
        name='Santander Account',
        type=AccountType.DETAIL,
    ),
    Account(
        id=constants.HSBC_ACCOUNT_ID,
        name='HSBC Account',
        type=AccountType.DETAIL,
    ),
    Account(
        id=constants.SCOTIABANK_ACCOUNT_ID,
        name='Scotiabank Account',
        type=AccountType.DETAIL,
    )
]
