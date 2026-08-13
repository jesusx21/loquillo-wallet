import asyncio
import inquirer
from uuid import UUID

from .fixtures import load_database
from database import get_database
from database.stores.errors import DatabaseError
from domain.entities import Entry, Transaction


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
        inquirer.Text(
            'amount',
            message="Type the transaction amount",
        ),
        inquirer.List(
            'source_wallet',
            message="Select the source wallet",
            choices=wallet_choices,
            carousel=True
        ),
        inquirer.List(
            'target_wallet',
            message="Select the target wallet",
            choices=wallet_choices,
            carousel=True
        )
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

    transaction_amount = float(answers['amount'])

    try:
        transaction = await database.transactions.create(
            Transaction(f'Transfer from {source_account.name} to {target_account.name}', transaction_amount)
        )

        source_entry = await database.entries.create(
            Entry(
                account=source_account,
                transaction_id=transaction.id,
                concept=f"Transfer to {target_account.name}",
                amount=-transaction_amount
            )
        )

        target_entry = await database.entries.create(
            Entry(
                account=target_account,
                transaction_id=transaction.id,
                concept=f"Transfer from {source_account.name}",
                amount=transaction_amount
            )
        )
    except Exception as error:
        raise UnexpectedError() from error

    print(f"Transaction created: {transaction.description}")
    for entry in [source_entry, target_entry]:
        print(f"{entry.concept}: ${entry.amount}")


if __name__ == "__main__":
    asyncio.run(main())
