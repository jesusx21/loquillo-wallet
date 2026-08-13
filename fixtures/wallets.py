from domain.entities import Wallet
from domain.entities.wallet import WalletType

wallets = [
    Wallet('Albo', WalletType.DEBIT_CARD),
    Wallet('BBVA', WalletType.DEBIT_CARD),
    Wallet('Cash', WalletType.CASH),
    Wallet('Hey', WalletType.DEBIT_CARD),
    Wallet('Nu', WalletType.DEBIT_CARD),
    Wallet('Spin', WalletType.DEBIT_CARD),
    Wallet('Stori', WalletType.DEBIT_CARD),
    Wallet('Didi', WalletType.DEBIT_CARD)
]
