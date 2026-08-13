import asyncio

from . import main as _main


if __name__ == "__main__":
    # `_main` is the coroutine function defined in `run_script.__init__`
    asyncio.run(_main())
