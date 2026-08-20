from unittest.mock import patch

from tests import TestCase
from .fixtures import load_fixtures, constants

from domain.entities.wallet import WalletType
from domain.errors import CouldNotGetWallets
from domain.use_cases import GetWallets


class TestGetWallets(TestCase):
    async def async_set_up(self):
        await super().async_set_up()

        self.database = self.get_database()

        await load_fixtures(self.database, ['accounts', 'wallets'])

    async def test_get_same_type_wallets(self):
        wallets = await self._get_wallets(wallet_type=[WalletType.DEBIT_CARD])

        self.assert_that(wallets).is_length(2)
        for wallet in wallets:
            self.assert_that(wallet.type.value).is_equal_to('debit_card')
            self.assert_that(wallet.user_id).is_equal_to(constants.FIRST_USER_ID)

    async def test_get_wallets_for_multiple_types(self):
        wallets = await self._get_wallets(wallet_type=[WalletType.DEBIT_CARD, WalletType.CASH])

        self.assert_that(wallets).is_length(4)
        for wallet in wallets:
            self.assert_that(wallet.type.value).is_in('debit_card', 'cash')
            self.assert_that(wallet.user_id).is_equal_to(constants.FIRST_USER_ID)

    async def test_get_wallets_for_all_types(self):
        wallets = await self._get_wallets(wallet_type=[
            WalletType.DEBIT_CARD,
            WalletType.CASH,
            WalletType.CREDIT_CARD
        ])

        self.assert_that(wallets).is_length(5)
        for wallet in wallets:
            self.assert_that(wallet.user_id).is_equal_to(constants.FIRST_USER_ID)
            self.assert_that(wallet.type.value).is_in(
                'debit_card',
                'cash',
                'credit_card'
            )

    async def test_get_wallets_return_empty_when_types_is_empty(self):
        wallets = await self._get_wallets(wallet_type=[])

        self.assert_that(wallets).is_equal_to([])

    async def test_get_wallets_returns_empty_list_when_no_wallet_matches(self):
        wallets = await self._get_wallets(
            user_id=constants.SECOND_USER_ID,
            wallet_type=[
                WalletType.DEBIT_CARD,
                WalletType.CASH,
                WalletType.CREDIT_CARD
            ]
        )

        self.assert_that(wallets).is_equal_to([])

    async def test_raises_could_not_get_wallets_when_database_fails(self):
        with patch.object(self.database.wallets, 'find') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(CouldNotGetWallets):
                await self._get_wallets(wallet_type=[WalletType.DEBIT_CARD])

    async def _get_wallets(self, user_id=constants.FIRST_USER_ID, wallet_type=None):
        get_wallets = GetWallets(
            self.database,
            user_id,
            wallet_types=wallet_type
        )

        return await get_wallets.execute()
