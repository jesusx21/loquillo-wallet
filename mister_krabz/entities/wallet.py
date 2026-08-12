from mister_krabz.entities.entity import Entity


class WalletAccountAlreadySet(Exception): pass
class WalletAccountNotSet(Exception): pass


class Wallet(Entity):
    def __init__(self, name, type, account_id, id=None, created_at=None, updated_at=None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)

        self.name = name
        self.type = type
        self.account_id = account_id
    
    # def set_wallet_account(self, wallet_account):
    #     if self._wallet_account:
    #         raise WalletAccountAlreadySet()

    #     self._wallet_account = wallet_account
    
    # async def get_account(self):
    #     if self._account:
    #         return self._account
        
    #     if not self._wallet_account:
    #         raise WalletAccountNotSet()
            
    #     self._account = await self._wallet_account.get_account()

    #     return self._account

