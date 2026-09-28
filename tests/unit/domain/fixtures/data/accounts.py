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
    ),
    Account(
        id=constants.NU_BANK_ACCOUNT_ID,
        name='Nu Bank Account',
        type=AccountType.DETAIL,
    ),
    Account(
        id=constants.BONUS_ACCOUNT_ID,
        name='Bonus Account',
        type=AccountType.DETAIL,
    ),
    Account(
        id=constants.DEPOSITS_ACCOUNT_ID,
        name='Deposits Account',
        type=AccountType.DETAIL,
    ),
    Account(
        id=constants.INVERSIONS_ACCOUNT_ID,
        name='Inversions Account',
        type=AccountType.DETAIL,
    ),
    Account(
        id=constants.PAYMENTS_ACCOUNT_ID,
        name='Payments Account',
        type=AccountType.DETAIL,
    ),
    Account(
        id=constants.WITHDRAWAL_ACCOUNT_ID,
        name='Withdrawal Account',
        type=AccountType.DETAIL,
    ),
    Account(
        id=constants.CLOTHING_ACCOUNT_ID,
        name='Clothing Account',
        type=AccountType.DETAIL,
    ),
    Account(
        id=constants.FOOD_ACCOUNT_ID,
        name='Food Account',
        type=AccountType.DETAIL,
    ),
    Account(
        id=constants.RENT_ACCOUNT_ID,
        name='Rent Account',
        type=AccountType.DETAIL,
    ),
    Account(
        id=constants.SAVINGS_ACCOUNT_ID,
        name='Savings Account',
        type=AccountType.DETAIL,
    ),
    Account(
        id=constants.TRANSPORTATION_ACCOUNT_ID,
        name='Transportation Account',
        type=AccountType.DETAIL,
    ),
    Account(
        id=constants.DEBT_ACCOUNT_ID,
        name='Debt Account',
        type=AccountType.DETAIL,
    ),
    Account(
        id=constants.LOAN_ACCOUNT_ID,
        name='Loan Account',
        type=AccountType.DETAIL,
    )
]
