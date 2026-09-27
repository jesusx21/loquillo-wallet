from uuid import UUID

from domain.crud import CRUD
from domain.crud.wallets.errors import WalletNotFound
from domain.entities import User, Wallet


class TransferFunds:
    def __init__(
        self,
        crud: CRUD,
        user: User,
        source_wallet_id: UUID,
        target_wallet_id: UUID,
        amount: float
    ):
        self.__crud = crud

        self.__user = user
        self.__source_wallet_id = source_wallet_id
        self.__target_wallet_id = target_wallet_id
        self.__amount = amount

    async def execute(self):
        source_wallet = await self._get_wallet(self.__source_wallet_id)
        target_wallet = await self._get_wallet(self.__target_wallet_id)

        return await self.__create_transaction(source_wallet, target_wallet)

    async def _get_wallet(self, wallet_id: UUID):
        wallet = await self.__crud.wallets.get_by_id(wallet_id)

        if wallet.user_id != self.__user.id:
            raise WalletNotFound(wallet_id=wallet_id)

        return wallet

    async def __create_transaction(self, source_wallet: Wallet, target_wallet: Wallet):
        return await self.__crud.transactions.create(
            source_wallet.account_id,
            target_wallet.account_id,
            f'Transfer to {target_wallet.name}.',
            f'Transfer from {source_wallet.name}.',
            self.__amount
        )
