from mister_krabz.entities.entity import Entity


class WalletCategory(Entity):
    def __init__(self, wallet, category, account, id=None, created_at=None, updated_at=None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)

        self._wallet = wallet
        self._category = category
        self._account = account
