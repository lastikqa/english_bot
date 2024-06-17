
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot
from aiogram.types import BotCommand
from lexicon.lexicon import menu_keyboard


def create_inline_kb(width: int,
                     last_btn: str | None = None,
                     *args: str,
                     **kwargs: str
                    ) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=button,
                callback_data=button))
    if kwargs:
        for text, button in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))
    kb_builder.row(*buttons, width=width)
    if last_btn :
        kb_builder.row(InlineKeyboardButton(
            text=last_btn,
            callback_data='menu_button'
        ))
    return kb_builder.as_markup()

async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in menu_keyboard.items()
    ]
    await bot.set_my_commands(main_menu_commands)