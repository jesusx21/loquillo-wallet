class CouldNotGetAccount(Exception): pass


class WalletAccount:
    def __init__(self, db, wallet, account_id):
        self._db = db
        self._wallet = wallet
        self._account_id = account_id
    
    async def get_account(self):
        try:
            return await self._db.accounts.find_by_id(self._account_id)
        except Exception as error:
            raise CouldNotGetAccount(error)