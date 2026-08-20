from . import constants

from domain.entities.wallet import Wallet, WalletType

wallets = [
    Wallet(
        id=constants.BBVA_WALLET_ID,
        name='BBVA Wallet',
        type=WalletType.CASH,
        user_id=constants.FIRST_USER_ID,
        account_id=constants.BBVA_ACCOUNT_ID
    ),
    Wallet(
        id=constants.CASH_WALLET_ID,
        name='Cash Wallet',
        type=WalletType.DEBIT_CARD,
        user_id=constants.FIRST_USER_ID,
        account_id=constants.CASH_ACCOUNT_ID
    ),
    Wallet(
        id=constants.SANTANDER_WALLET_ID,
        name='Santander Wallet',
        type=WalletType.CREDIT_CARD,
        user_id=constants.FIRST_USER_ID,
        account_id=constants.SANTANDER_ACCOUNT_ID
    ),
    Wallet(
        id=constants.HSBC_WALLET_ID,
        name='HSBC Wallet',
        type=WalletType.CASH,
        user_id=constants.FIRST_USER_ID,
        account_id=constants.HSBC_ACCOUNT_ID
    ),
    Wallet(
        id=constants.SCOTIABANK_WALLET_ID,
        name='Scotiabank Wallet',
        type=WalletType.DEBIT_CARD,
        user_id=constants.FIRST_USER_ID,
        account_id=constants.SCOTIABANK_ACCOUNT_ID
    )
]
