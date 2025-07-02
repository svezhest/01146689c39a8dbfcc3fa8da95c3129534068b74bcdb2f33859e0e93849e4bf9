import asyncio
import logging
import sys

from data.config import BOT_TOKEN
from loader import dp, bot


async def main() -> None:
    from handlers import dp
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    