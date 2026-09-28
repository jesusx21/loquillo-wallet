from datetime import datetime
from uuid import UUID

from database import Database
from domain.crud import CRUD
from domain.entities import User, Wallet
from domain.entities.category import Category
from domain.entities.wallet import WalletType
from domain.use_cases import AddTransaction, CreateWallet, TransferFunds
from run_script.prompt import Prompt, SelectChoice


class Wallets:
    def __init__(self, database: Database, crud: CRUD):
        self._database = database
        self._crud = crud
        self._user = None
        self._wallets = []

    def set_user(self, user: User):
        self._user = user

    async def add_expense_transaction(self):
        categories = await self._crud.categories.get_expense(self._user.id)

        return await self.__add_transaction(categories)

    async def add_income_transaction(self):
        categories = await self._crud.categories.get_income(self._user.id)

        return await self.__add_transaction(categories)

    async def create(self):
        wallet_name = Prompt.string('Enter the wallet name')
        wallet_type = Prompt.select(
            message='Select the wallet type',
            choices=[
                SelectChoice(WalletType.CASH, 'Cash'),
                SelectChoice(WalletType.CREDIT_CARD, 'Credit Card'),
                SelectChoice(WalletType.DEBIT_CARD, 'Debit Card')
            ]
        )

        Prompt.echo(
            f'The Wallet of type \'{wallet_type.value}\' is being created: \'{wallet_name}\'...'
        )
        should_continue = Prompt.confirm('Do you want to continue?')

        if not should_continue:
            Prompt.echo('Wallet creation aborted.')
            return

        create_wallet = CreateWallet(
            self._database,
            self._crud,
            self._user.id,
            wallet_name,
            wallet_type
        )

        created_wallet = await create_wallet.execute()

        self._wallets.append(created_wallet)

        Prompt.echo(f'Wallet \'{created_wallet.name}\' created with ID: {created_wallet.id}')

    async def get_list(self):
        wallet_types = Prompt.checkbox(
            message='Select the wallet types to retrieve',
            choices=[
                SelectChoice(WalletType.CASH, 'Cash'),
                SelectChoice(WalletType.CREDIT_CARD, 'Credit Card'),
                SelectChoice(WalletType.DEBIT_CARD, 'Debit Card')
            ]
        )

        wallets = await self.__get_wallets(wallet_types)

        if not wallets:
            Prompt.echo('No wallets found for the selected types.')
            return

        self._wallets = wallets

        Prompt.echo('Retrieved Wallets:')
        for wallet in wallets:
            Prompt.echo(f'ID: {wallet.id}, Name: {wallet.name}, Type: {wallet.type.value}')

    async def transfer_funds(self):
        wallet_choices, wallets_by_id = await self.__build_wallets_options()

        wallets = await self.__get_wallets([
            WalletType.CASH,
            WalletType.CREDIT_CARD,
            WalletType.DEBIT_CARD
        ])

        for wallet in wallets:
            wallets_by_id[wallet.id] = wallet
            wallet_choices.append(SelectChoice(wallet.id, wallet.name))

        source_wallet_id = Prompt.select(
            message='Select the source wallet',
            choices=wallet_choices
        )
        source_wallet = wallets_by_id[source_wallet_id]
        Prompt.echo(f'Source wallet selected: {source_wallet.name}')

        target_wallet_id = Prompt.select(
            message='Select the target wallet',
            choices=wallet_choices
        )
        target_wallet = wallets_by_id[target_wallet_id]
        Prompt.echo(f'Target wallet selected: {target_wallet.name}')

        amount = Prompt.money('Enter the transaction amount') * 100

        transfer_funds = TransferFunds(
            self._crud,
            self._user,
            source_wallet_id,
            target_wallet_id,
            amount
        )

        transaction = await transfer_funds.execute()

        Prompt.echo('Transaction created')
        for entry in transaction.entries:
            Prompt.echo(f'{entry.concept}: ${entry.amount / 100.0:,.2f}')

    async def __get_wallets(self, types: list[WalletType]):
        return await self._crud.wallets.get_by_types(self._user.id, types)

    async def __build_categories_options(self, categories: list[Category]):
        categories_by_id: dict[UUID, Category] = {}
        category_choices: list[SelectChoice] = []

        for category in categories:
            categories_by_id[category.id] = category
            category_choices.append(SelectChoice(category.id, category.name))

        return category_choices, categories_by_id

    async def __build_wallets_options(self):
        wallets_by_id: dict[UUID, Wallet] = {}
        wallet_choices: list[SelectChoice] = []

        wallets = await self.__get_wallets([
            WalletType.CASH,
            WalletType.CREDIT_CARD,
            WalletType.DEBIT_CARD
        ])

        for wallet in wallets:
            wallets_by_id[wallet.id] = wallet
            wallet_choices.append(SelectChoice(wallet.id, wallet.name))

        return wallet_choices, wallets_by_id

    async def __add_transaction(self, categories: list[Category]):
        wallet_choices, wallets_by_id = await self.__build_wallets_options()

        wallet_id = Prompt.select(
            message='Select the wallet',
            choices=wallet_choices
        )
        wallet = wallets_by_id[wallet_id]
        Prompt.echo(f'Wallet selected: {wallet.name}')

        category_choices, categories_by_id = await self.__build_categories_options(categories)

        category_id = Prompt.select(
            message='Select the category',
            choices=category_choices
        )
        category = categories_by_id[category_id]
        Prompt.echo(f'Category selected: {category.name}')

        amount = Prompt.money('Enter the transaction amount') * 100

        should_add_date = Prompt.confirm(
            'Do you want to add a date for this transaction? (default is current date)'
        )
        date = Prompt.date('Enter the transaction date') if should_add_date else datetime.now()

        should_add_note = Prompt.confirm('Do you want to add a note for this transaction?')
        note = Prompt.string('Add note') if should_add_note else None

        add_transaction = AddTransaction(
            self._crud,
            self._user,
            wallet_id,
            category_id,
            amount,
            date,
            note
        )

        transaction = await add_transaction.execute()

        Prompt.echo('Transaction created')
        entry = transaction.source_entry if category.is_expense else transaction.target_entry
        Prompt.echo(f'{entry.concept}: ${entry.amount / 100.0:,.2f}')
