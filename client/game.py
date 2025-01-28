from typing import Literal, Any

from messages import GameMessage
from services.server.client import ServerService
from services.server.schemas import UserItemInSchema


class GameProcessService:
    GAME_SESSION_STATE: Literal["LOGIN", "GAME_SESSION"] = "LOGIN"
    IN_GAME: bool = True
    USER_ID: int | None = None

    CANCEL_CODE: str = "0"
    APPLY_CODE: str = "1"

    def __init__(self, api_client) -> None:
        self.client = ServerService(api_client)

    async def start_game(self) -> None:
        username = input(GameMessage.WELCOME).strip()
        login_response = await self.client.login(username)
        self._validate_response(login_response)

        self.GAME_SESSION_STATE = "GAME_SESSION"
        self.USER_ID = login_response.user.id

        await self.process_main_menu()

    async def process_main_menu(self) -> None:
        user = await self.client.get_user_by_id(self.USER_ID)
        menu_command = input(
            GameMessage.GAME_SESSION_START.format(
                nickname=user.username,
                credits=user.finance.balance,
                items_count=len(user.items),
            )
        )
        await self._process_menu_command(menu_command)

    async def _process_menu_command(self, command_number: str) -> None:
        menu_commands = {
            "1": self.all_items,
            "2": self.sell_item,
            "3": self.show_balance,
            "4": self.logout,
        }
        if command_number.strip() in menu_commands:
            await menu_commands[command_number.strip()]()
        else:
            command_number = input(GameMessage.INVALID_MENU_COMMAND)
            await self._process_menu_command(command_number)

    async def all_items(self) -> None:
        all_items = await self.client.get_all_items()
        self._validate_response(all_items)

        item_id = input(
            GameMessage.ALL_ITEMS.format(
                numerated_items="\n".join(
                    [f"{item.id}. {item.name} ({item.price})" for item in all_items]
                ),
            )
        )
        if item_id.strip() == self.CANCEL_CODE:
            await self.process_main_menu()
        else:
            await self._apply_buy_item(item_id, all_items)

    async def _apply_buy_item(
        self, item_id: str, items: list[UserItemInSchema]
    ) -> None:
        mapped_items = {item.id: item for item in items}

        if item_id.isdigit() and int(item_id) in mapped_items:
            user = await self.client.get_user_by_id(self.USER_ID)
            item = mapped_items[int(item_id)]
            apply_buy_item = input(
                GameMessage.BUY_ITEM.format(
                    item_name=item.name,
                    price=item.price,
                    new_balance=user.finance.balance - item.price,
                )
            )

            if apply_buy_item.strip() == self.APPLY_CODE:
                await self.buy_item(item_id)
            else:
                await self.process_main_menu()
        else:
            print(GameMessage.ITEM_NOT_FOUND)
            await self.all_items()

    async def buy_item(self, item_id: str) -> None:
        buy_item_result = await self.client.buy_item(self.USER_ID, item_id)
        await self._validate_item_action_response(buy_item_result)

        print(GameMessage.BUY_SUCCESS)
        await self.process_main_menu()

    async def sell_item(self) -> None:
        items = await self.client.get_user_items(self.USER_ID)

        if not items:
            print(GameMessage.ITEMS_EMPTY)
            return await self.process_main_menu()

        item_id = input(
            GameMessage.SELL_ITEM.format(
                numerated_items="\n".join(
                    [f"{item.id}. {item.name} ({item.price})" for item in items]
                ),
            )
        )

        if item_id.strip() == self.CANCEL_CODE:
            await self.process_main_menu()
        else:
            await self._apply_sell_item(item_id, items)

    async def _apply_sell_item(
        self, item_id: str, items: list[UserItemInSchema]
    ) -> None:
        mapped_items = {item.id: item for item in items}

        if item_id.isdigit() and int(item_id) in mapped_items:
            item = mapped_items[int(item_id)]
            apply_sell_item = input(
                GameMessage.SELL_ITEM_APPLY.format(item_name=item.name)
            )

            if apply_sell_item.strip() == self.APPLY_CODE:
                await self.sell_item_process(item_id)
            else:
                await self.process_main_menu()
        else:
            print(GameMessage.ITEM_NOT_FOUND)
            await self.sell_item()

    async def sell_item_process(self, item_id: str) -> None:
        sold = await self.client.sell_item(self.USER_ID, item_id)
        await self._validate_item_action_response(sold)

        print(GameMessage.SELL_SUCCESS)
        await self.process_main_menu()

    async def show_balance(self) -> None:
        user_finances = await self.client.get_balance(self.USER_ID)
        self._validate_response(user_finances)

        print(GameMessage.BALANCE.format(credits=user_finances.balance))
        await self.process_main_menu()

    async def logout(self) -> None:
        print(GameMessage.LOGOUT)
        self.GAME_SESSION_STATE = "LOGIN"
        self.IN_GAME = False

    def _validate_response(self, response: Any) -> None:
        if response is None:
            print(GameMessage.SERVER_UNREACHABLE)
            self.IN_GAME = False

    async def _validate_item_action_response(self, response: Any) -> None:
        self._validate_response(response)

        if response.get("status"):
            match response["detail"]:
                case "NOT_ENOUGH_BALANCE":
                    print(GameMessage.NOT_ENOUGH_BALANCE)
                    await self.all_items()
                case "ALREADY_HAVE_ITEM":
                    print(GameMessage.ALREADY_HAVE_ITEM)
                    await self.all_items()
                case _:
                    print(GameMessage.CANT_DO_IT)
                    await self.all_items()
