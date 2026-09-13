import asyncio
import sys

import click

from . import main as _main
from .prompt import Prompt

if __name__ == '__main__':
    # `_main` is the coroutine function defined in `run_script.__init__`
    try:
        asyncio.run(_main())
    except (KeyboardInterrupt, click.Abort, asyncio.CancelledError):
        Prompt.echo('\nExecution cancelled by user.')
        sys.exit(0)
