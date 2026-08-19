import asyncio

from app.config import Config
from database import get_database

# from .fixtures import load_database
from .menu import Menu


async def main():
    config = Config('config.ini')
    database = get_database(config)

    # await load_database(database)

    menu = Menu(database)
    await menu.display()

if __name__ == "__main__":
    asyncio.run(main())
