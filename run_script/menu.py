import sys

from database import Database
from run_script.resources.wallets import Wallets
from .prompt import Prompt, SelectChoice
from .resources.users import Users


class MenuItem:
    def __init__(self, name: str, action: callable):
        self.name = name
        self.action = action

    async def run(self):
        await self.action()


class Menu:
    def __init__(self, database: Database):
        self._database = database
        self.users_resource = Users(database)
        self.wallets_resource = Wallets(database)

        self._main_menu_items = {
            'create_wallet': MenuItem('Create a Wallet', self.wallets_resource.create),
            'get_wallets': MenuItem('Get Wallets', self.wallets_resource.get_list),
            'transfer_funds': MenuItem('Transfer Funds', self.wallets_resource.transfer_funds),
            'sign_out': MenuItem('Sign Out', self.users_resource.sign_out),
            'exit': MenuItem('Exit', self._exit)
        }
        self.users_items = {
            'sign_up': MenuItem('Sign Up', self.users_resource.sign_up),
            'sign_in': MenuItem('Sign In', self.users_resource.sign_in),
            'exit': MenuItem('Exit', self._exit)
        }

    async def display(self):
        if self.users_resource.is_authenticated():
            user = self.users_resource.get_current_user()
            self.wallets_resource.set_user_id(user.id)
            await self._display_menu(self._main_menu_items)
        else:
            await self._display_menu(self.users_items)

        return await self.display()

    async def _display_menu(self, items: dict[str, MenuItem]):
        choices = [SelectChoice(key, item.name) for key, item in items.items()]

        selected_option = Prompt.select(
            message='Select an option',
            choices=choices
        )

        if selected_option in items:
            await items[selected_option].run()

    async def _exit(self):
        if self.users_resource.is_authenticated():
            Prompt.echo('Signing out before exit...')
            await self.users_resource.sign_out()

        Prompt.echo('Exiting...')
        sys.exit(0)
