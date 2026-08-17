from . import constants

from database.tables import Wallets
from domain.entities.wallet import WalletType

wallet_fixtures = {
    'table': Wallets,
    'data': [
        {
            'id': constants.ALBO_WALLET_ID,
            'name': 'Albo',
            'account_id': constants.ALBO_ACCOUNT_ID,
            'type': WalletType.DEBIT_CARD.value,
            'user_id': constants.USER_ID
        },
        {
            'id': constants.BBVA_WALLET_ID,
            'name': 'BBVA',
            'account_id': constants.BBVA_ACCOUNT_ID,
            'type': WalletType.CREDIT_CARD.value,
            'user_id': constants.SECOND_USER_ID
        },
        {
            'id': constants.NU_BANK_WALLET_ID,
            'name': 'Nu Bank',
            'account_id': constants.NU_BANK_ACCOUNT_ID,
            'type': WalletType.DEBIT_CARD.value,
            'user_id': constants.THIRD_USER_ID
        },
        {
            'id': constants.STORI_WALLET_ID,
            'name': 'Stori',
            'account_id': constants.STORI_ACCOUNT_ID,
            'type': WalletType.CREDIT_CARD.value,
            'user_id': constants.USER_ID
        },
        {
            'id': constants.HSBC_WALLET_ID,
            'name': 'HSBC',
            'account_id': constants.HSBC_ACCOUNT_ID,
            'type': WalletType.DEBIT_CARD.value,
            'user_id': constants.SECOND_USER_ID
        }
    ]
}
