from uuid import UUID

from .errors import InvalidCategoryType, InvalidTransactionAmount
from domain.crud import CRUD
from domain.crud.categories.errors import CategoryNotFound
from domain.crud.wallets.errors import WalletNotFound
from domain.entities import User


class AddTransaction:
    def __init__(
        self,
        crud: CRUD,
        user: User,
        wallet_id: UUID,
        category_id: UUID,
        amount: int,
        date: str,
        note: str = None
    ):
        self.__crud = crud
        self.__user = user
        self.__wallet_id = wallet_id
        self.__category_id = category_id
        self.__amount = amount
        self.__date = date
        self.__note = note

    async def execute(self):
        category = await self.__crud.categories.get_by_id(self.__category_id)

        if (category.user_id != self.__user.id):
            raise CategoryNotFound(self.__category_id)

        wallet = await self.__crud.wallets.get_by_id(self.__wallet_id)

        if (wallet.user_id != self.__user.id):
            raise WalletNotFound(self.__wallet_id)

        if (self.__amount <= 0):
            raise InvalidTransactionAmount(self.__amount)

        if category.is_income():
            source_account_id = category.account_id
            target_account_id = wallet.account_id
        elif category.is_expense():
            source_account_id = wallet.account_id
            target_account_id = category.account_id
        else:
            raise InvalidCategoryType(category.type)

        return await self.__crud.transactions.create(
            source_account_id=source_account_id,
            source_concept=category.name,
            target_account_id=target_account_id,
            target_concept=category.name,
            amount=self.__amount,
            date=self.__date,
            note=self.__note
        )
