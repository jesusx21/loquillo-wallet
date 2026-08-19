from tests.database.sql import SQLTestCase

from database.stores.sql import SQLTransactionDatabase
from database.stores.sql.errors import TransactionNotOpened
from database.tables import Users


class TestSQLTransactions(SQLTestCase):
    async def async_set_up(self):
        await super().async_set_up()

        self.database = self.get_database()

    async def async_tear_down(self):
        await super().async_tear_down()

    async def test_transaction_commits_entity_creation(self):
        async with self.database.transacting() as transaction_db:
            result = await transaction_db.execute(
                Users.insert().values(
                    names='Alice',
                    last_names='Miller',
                    email='alice@example.com'
                ).returning('*')
            )
            row = result.first()

            self.assertTrue(transaction_db.is_transacting())
            self.assertEqual(row['email'], 'alice@example.com')

        result = await self.database.execute(
            Users.select().where(Users.c.email == 'alice@example.com')
        )
        row = result.first()

        self.assertIsNotNone(row)
        self.assertEqual(row['email'], 'alice@example.com')

    async def test_transaction_rolls_back_on_exception(self):
        with self.assertRaises(ValueError):
            async with self.database.transacting() as transaction_db:
                await transaction_db.execute(
                    Users.insert().values(
                        names='Bob',
                        last_names='Smith',
                        email='bob@example.com'
                    )
                )
                self.assertTrue(transaction_db.is_transacting())
                raise ValueError('rollback requested')

        result = await self.database.execute(
            Users.select().where(Users.c.email == 'bob@example.com')
        )

        self.assertIsNone(result.first())

    async def test_execute_requires_an_open_transaction(self):
        transaction_db = SQLTransactionDatabase(self.engine)

        self.assertFalse(transaction_db.is_transacting())

        with self.assertRaises(TransactionNotOpened):
            await transaction_db.execute(Users.select())
