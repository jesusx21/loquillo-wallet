import asyncio
import sys

import click

from app.config import Config
from database import get_database

# from .fixtures import load_database
from .menu import Menu
from .prompt import Prompt


async def main():
    try:
        config = Config('config.ini')
        database = get_database(config)

        # await load_database(database)

        menu = Menu(database)
        await menu.display()
    except (KeyboardInterrupt, click.Abort, asyncio.CancelledError):
        Prompt.echo('\nExecution cancelled by user.')
        sys.exit(0)


if __name__ == '__main__':
    asyncio.run(main())
