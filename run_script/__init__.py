import asyncio
from uuid import UUID

import inquirer

from database import get_database
from database.stores.errors import DatabaseError
from domain.entities import Entry, Transaction
from run_script.fixtures import load_database


class CouldNotFindSourceAccount(Exception):
    pass


class CouldNotFindTargetAccount(Exception):
    pass


class UnexpectedError(Exception):
    pass


async def main():
    database = get_database()

    await load_database(database)

    wallets = await database.wallets.find_list()

    wallet_choices = [f'{wallet.id}: {wallet.name}' for wallet in wallets]

    questions = [
        inquirer.Text('amount', message="Type the transaction amount"),
        inquirer.List(
            'source_wallet',
            message="Select the source wallet",
            choices=wallet_choices,
            carousel=True,
        ),
        inquirer.List(
            'target_wallet',
            message="Select the target wallet",
            choices=wallet_choices,
            carousel=True,
        ),
    ]

    # inquirer.prompt is blocking; run it in a thread so we don't block the loop
    answers = await asyncio.to_thread(inquirer.prompt, questions)

    try:
        source_wallet_id = UUID(answers['source_wallet'].split(': ')[0])
        source_wallet = await database.wallets.find_by_id(source_wallet_id)
        source_account = source_wallet.account
    except DatabaseError as error:
        raise CouldNotFindSourceAccount() from error
    except Exception as error:
        raise UnexpectedError() from error

    try:
        target_wallet_id = UUID(answers['target_wallet'].split(': ')[0])
        target_wallet = await database.wallets.find_by_id(target_wallet_id)
        target_account = target_wallet.account
    except DatabaseError as error:
        raise CouldNotFindTargetAccount() from error
    except Exception as error:
        raise UnexpectedError() from error

    transaction_amount = float(answers['amount']) * 100

    try:
        transaction = Transaction(
            f'Transfer from {source_account.name} to {target_account.name}'
        )

        transaction.add_entries(
            Entry(
                account=source_account,
                concept=f"Transfer to {target_account.name}",
                amount=-transaction_amount
            ),
            Entry(
                account=target_account,
                concept=f"Transfer from {source_account.name}",
                amount=transaction_amount
            )
        )

        transaction = await database.transactions.create(transaction)
    except Exception as error:
        raise UnexpectedError() from error

    print(f"Transaction created: {transaction.description}")
    for entry in transaction.entries:
        print(f"{entry.concept}: ${entry.amount / 100.0}")


if __name__ == "__main__":
    asyncio.run(main())
