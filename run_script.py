import asyncio
import inquirer
from uuid import UUID

from fixtures import load_database
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

    accounts = await database.accounts.find_list()

    accounts_choices = [f'{account.id}: {account.name}' for account in accounts]

    questions = [
        inquirer.Text(
            'description',
            message="Type the transaction description",
        ),
        inquirer.Text(
            'amount',
            message="Type the transaction amount",
        ),
        inquirer.List(
            'source_account',
            message="Select the source account",
            choices=accounts_choices,
            carousel=True
        ),
        inquirer.List(
            'target_account',
            message="Select the target account",
            choices=accounts_choices,
            carousel=True
        )
    ]

    # inquirer.prompt is blocking; run it in a thread so we don't block the loop
    answers = await asyncio.to_thread(inquirer.prompt, questions)

    try:
        source_account_id = UUID(answers['source_account'].split(': ')[0])
        source_account = await database.accounts.find_by_id(source_account_id)
    except DatabaseError as error:
        raise CouldNotFindSourceAccount() from error
    except Exception as error:
        raise UnexpectedError() from error

    try:
        target_account_id = UUID(answers['target_account'].split(': ')[0])
        target_account = await database.accounts.find_by_id(target_account_id)
    except DatabaseError as error:
        raise CouldNotFindTargetAccount() from error
    except Exception as error:
        raise UnexpectedError() from error

    transaction_amount = float(answers['amount'])

    try:
        transaction = await database.transactions.create(
            Transaction(answers['description'])
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
