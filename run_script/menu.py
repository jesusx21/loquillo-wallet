import sys

from database.stores import InMemoryDatabase
from domain.entities import Entry, Transaction, Wallet
from domain.entities.wallet import WalletType

from .prompt import Prompt, SelectChoice


class MenuItem:
    def __init__(self, name: str, action: callable):
        self.name = name
        self.action = action

    async def run(self):
        await self.action()


class Menu:
    def __init__(self, database: InMemoryDatabase):
        self._database = database

        self.items = {
            'create_wallet': MenuItem('Create a Wallet', self._create_wallet),
            'transfer_funds': MenuItem('Transfer Funds', self._transfer_funds),
            'exit': MenuItem('Exit', self._exit)
        }

    async def display(self):
        choices = [SelectChoice(key, item.name) for key, item in self.items.items()]
        selected_option = Prompt.select(
            message='Select an option',
            choices=choices
        )

        if selected_option in self.items:
            await self.items[selected_option].run()

        return await self.display()

    async def _create_wallet(self):
        wallet_name = Prompt.string('Enter the wallet name')
        wallet_type = Prompt.select(
            message='Select the wallet type',
            choices=[
                SelectChoice(WalletType.CASH, 'Efectivo'),
                SelectChoice(WalletType.CREDIT_CARD, 'Tarjeta de Crédito'),
                SelectChoice(WalletType.DEBIT_CARD, 'Tarjeta de Débito')
            ]
        )

        wallet = Wallet(wallet_name, type=WalletType(wallet_type))

        Prompt.echo(
            f'The Wallet of type \'{wallet.type.value}\' is being created: \'{wallet.name}\'...'
        )
        should_continue = Prompt.confirm('Do you want to continue?')

        if not should_continue:
            Prompt.echo('Wallet creation aborted.')
            return

        created_wallet = await self._database.wallets.create(wallet)

        Prompt.echo(f'Wallet \'{created_wallet.name}\' created with ID: {created_wallet.id}')

    async def _exit(self):
        Prompt.echo('Exiting...')
        sys.exit(0)

    async def _transfer_funds(self):
        wallets = await self._database.wallets.find_list()
        wallets_by_id = {}
        wallet_choices = []

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

        description = f'Transfer from {source_wallet.name} to {target_wallet.name}'
        amount = Prompt.money('Enter the transaction amount') * 100

        transaction = Transaction(description)
        transaction.add_entries(
            Entry(
                account=source_wallet.account,
                transaction_id=transaction.id,
                concept=f'Transfer to {target_wallet.name}',
                amount=-int(amount)
            ),
            Entry(
                account=target_wallet.account,
                transaction_id=transaction.id,
                concept=f'Transfer from {source_wallet.name}',
                amount=int(amount)
            )
        )

        Prompt.echo(f'Transaction created: {transaction.description}')
        for entry in transaction.entries:
            Prompt.echo(f'{entry.concept}: ${entry.amount / 100.0:,.2f}')
