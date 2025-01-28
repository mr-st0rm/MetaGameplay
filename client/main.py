import asyncio
import logging

from config.cfg import get_config
from services.api_client.aiohttp_client import AioHttpClient
from game import GameProcessService


async def main():
    # чтобы логи и стандартный вывод не пересекались и не мешали игровому процессу
    logging.basicConfig(
        handlers=[logging.FileHandler("log.txt", "a", "utf-8")],
        level=logging.INFO,
        format="{%(pathname)s:%(lineno)d} %(asctime)s - %(levelname)s - %(message)s",
    )
    config = get_config()

    aiohttp_client = AioHttpClient(config.api.BASE_URL)
    game_service = GameProcessService(aiohttp_client)

    try:
        while game_service.IN_GAME:
            await game_service.start_game()
    finally:
        await aiohttp_client.client.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Очень жаль что вы уходите, я буду вас ждать...")
