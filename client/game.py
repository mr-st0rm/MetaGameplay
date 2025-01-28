import os
from typing import Literal

from client.messages import GameMessage
from client.services.server.client import ServerService
from client.services.server.schemas import UserLoginInSchema


class GameProcessService:
    GAME_SESSION_STATE: Literal["LOGIN", "GAME_SESSION"] = "LOGIN"
    IN_GAME: bool = True

    def __init__(self, api_client) -> None:
        self.client = ServerService(api_client)

    async def start_game(self) -> None:
        username = input(GameMessage.WELCOME).strip()
        login_response = await self.client.login(username)

        if not login_response:
            print(GameMessage.SERVER_UNREACHABLE)
            self.IN_GAME = False

        self.GAME_SESSION_STATE = "GAME_SESSION"

        await self.process_main_menu(login_response)

    async def process_main_menu(self, login_response: UserLoginInSchema) -> None:
        self._clear_output()
        menu_command = input(
            GameMessage.GAME_SESSION_START.format(
                nickname=login_response.user.username,
                credits=login_response.user.finance.balance,
                items_count=len(login_response.user.items),
            )
        )
        await self._process_menu_command(menu_command)

    async def _process_menu_command(self, command_number: str) -> None: ...

    def _clear_output(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")
