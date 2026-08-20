from uuid import UUID

from database import Database
from domain.entities.transaction import TransactionStatus
from domain.entities.wallet import WalletType
from domain.use_cases.create_wallet import CreateWallet
from domain.use_cases.get_wallets import GetWallets
from run_script.prompt import Prompt, SelectChoice
from domain.entities import Entry, Transaction


class Wallets:
    def __init__(self, database: Database):
        self._database = database
        self._user_id = None
        self._wallets = []

    def set_user_id(self, user_id: UUID):
        self._user_id = user_id

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

        create_wallet = CreateWallet(self._database, self._user_id, wallet_name, wallet_type)

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

        get_wallets = GetWallets(self._database, self._user_id, wallet_types)

        wallets = await get_wallets.execute()

        if not wallets:
            Prompt.echo('No wallets found for the selected types.')
            return

        self._wallets = wallets

        Prompt.echo('Retrieved Wallets:')
        for wallet in wallets:
            Prompt.echo(f'ID: {wallet.id}, Name: {wallet.name}, Type: {wallet.type.value}')

    async def transfer_funds(self):
        wallets_by_id = {}
        wallet_choices = []

        for wallet in self._wallets:
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

        transaction = Transaction(description, TransactionStatus.PENDING)
        transaction.add_entries(
            Entry(
                account_id=source_wallet.account_id,
                transaction_id=transaction.id,
                concept=f'Transfer to {target_wallet.name}',
                amount=-int(amount)
            ),
            Entry(
                account_id=target_wallet.account_id,
                transaction_id=transaction.id,
                concept=f'Transfer from {source_wallet.name}',
                amount=int(amount)
            )
        )

        Prompt.echo(f'Transaction created: {transaction.description}')
        for entry in transaction.entries:
            Prompt.echo(f'{entry.concept}: ${entry.amount / 100.0:,.2f}')
