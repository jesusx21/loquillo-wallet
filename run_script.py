import inquirer

from fixtures import accounts
from entities import Entry, Transaction

accounts_choices = [account.name for account in accounts.values()]

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

answers = inquirer.prompt(questions)

source_account = None
target_account = None

for account in accounts.values():
    if account.name == answers['source_account']:
        source_account = account
    elif account.name == answers['target_account']:
        target_account = account

if source_account is None or target_account is None:
    print("Error: Invalid account selection.")
    exit(1)
    
transaction_description = answers['description']
transaction_amount = float(answers['amount'])

source_entry = Entry(
    account=source_account,
    concept=f"Transfer to {target_account.name}",
    amount=-transaction_amount
)
target_entry = Entry(
    account=target_account,
    concept=f"Transfer from {source_account.name}",
    amount=transaction_amount
)

transaction = Transaction(
    description=transaction_description,
    entries=[source_entry, target_entry]
)

print(f"Transaction created: {transaction.description}")
for entry in transaction.entries:
    print(f"{entry.concept}: ${entry.amount}")
