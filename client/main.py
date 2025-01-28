import asyncio
import logging

from client.config.cfg import get_config
from client.services.api_client.aiohttp_client import AioHttpClient
from client.game import GameProcessService


async def main():
    # чтобы логи и стандартный вывод не пересекались и не мешали игровому процессу
    logging.basicConfig(
        handlers=[logging.FileHandler("log.txt", "a", "utf-8")],
        level=logging.INFO,
        format="{%(pathname)s:%(lineno)d} %(asctime)s - %(levelname)s - %(message)s",
    )
    config = get_config()

    game_service = GameProcessService(AioHttpClient(config.api.BASE_URL))

    while game_service.IN_GAME:
        await game_service.start_game()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Очень жаль что вы уходите, я буду вас ждать...")
