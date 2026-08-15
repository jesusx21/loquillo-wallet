import asyncio

from database import get_database

from .fixtures import load_database
from .menu import Menu


async def main():
    database = get_database()

    await load_database(database)

    menu = Menu(database)
    await menu.display()

if __name__ == "__main__":
    asyncio.run(main())
