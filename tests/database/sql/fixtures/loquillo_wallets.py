from . import constants

from database.tables import LoquilloWallets

loquillo_wallet_fixtures = {
    'table': LoquilloWallets,
    'data': [
        {
            'id': constants.LOQUILLO_WALLET_ID,
            'user_id': constants.USER_ID,
            'incomes_account_id': constants.ALBO_ACCOUNT_ID,
            'expenses_account_id': constants.BBVA_ACCOUNT_ID,
        },
        {
            'id': constants.SECOND_LOQUILLO_WALLET_ID,
            'user_id': constants.SECOND_USER_ID,
            'incomes_account_id': constants.NU_BANK_ACCOUNT_ID,
            'expenses_account_id': constants.STORI_ACCOUNT_ID,
        }
    ]
}
