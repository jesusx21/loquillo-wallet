from database import Database
from run_script.prompt import Prompt
from domain.use_cases import CreateUser


class Users:
    def __init__(self, database: Database):
        self._database = database
        self._user = None

    async def sign_in(self):
        email = Prompt.email('Enter the email address')

        # TODO: Use find_by_email method instead of directly accessing the database
        try:
            self._user = await self._database.users._find_one(email=email)
        except Exception as error:
            Prompt.echo(f'No user found with email: {email}. Error: {error}')
            return

        Prompt.echo(f'Welcome {self._user.names}!!')

    async def sign_up(self):
        user_name = Prompt.string('Enter the first and middle name')
        last_names = Prompt.string('Enter the last names')
        email = Prompt.email('Enter the email address')

        create_user = CreateUser(self._database, user_name, last_names, email)

        self._user = await create_user.execute()
        Prompt.echo(f'User \'{user_name}\' created successfully!')

    async def sign_out(self):
        # Logic to sign out the current user
        self._user = None

    def get_current_user(self):
        return self._user

    def is_authenticated(self):
        return self._user is not None
