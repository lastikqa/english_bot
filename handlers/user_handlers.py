from aiogram import Bot
import time
from config import token
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import start_keyboard, help_message, default_menu
from lexicon.user_handlers_lexicon import languages
from english_bot_database.english_bot_database import EnglishBotDatabase
from aiogram import Router
from data.file_manager import FileManager


router = Router()
time.sleep(2)
bot = Bot(token=token)


@router.message(CommandStart())
async def process_start_command(message: Message):
    message_id = message.message_id
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    user_id = message.from_user.id
    database = EnglishBotDatabase(user_id)

    if database.looking_for_user_in_db(user_id=user_id) is False:
        database.creating_object_user_in_db(user_id, first_name)
    keyboard = create_inline_kb(1, **start_keyboard)
    await message.answer(text="Hello. Choose something", reply_markup=keyboard)
    await bot.delete_message(chat_id, message_id)


@router.message()
async def menu_button(message: Message):
    """the function processes menu button"""
    user_id = message.from_user.id
    database = EnglishBotDatabase(user_id)
    message_id = message.message_id
    chat_id = message.chat.id
    message = message.text
    if message.text == "/help":
        keyboard = create_inline_kb(1, last_btn=default_menu)
        await message.answer(text=help_message, parse_mode="MarkdownV2", reply_markup=keyboard)

    if message == "/translation":
        translation = database.checking_user_translation(user_id=message.from_user.id)
        language = database.checking_user_language(user_id=user_id)

        translation, language = language, translation
        database.updating_user_translation(translation=translation, user_id=message.from_user.id)
        database.updating_user_language(language=language, user_id=user_id)

    if "!setnicname" in message.split()[0].lower():
        nickname = message.text.split()[1]
        database.updating_user_first_name(user_id=message.from_user.id, nickname=nickname)

    if message == '/scores':
        text = database.getting_user_scores(user_id=message.from_user.id)
        keyboard = create_inline_kb(1, last_btn=default_menu)
        await message.answer(text=text, parse_mode="MarkdownV2", reply_markup=keyboard)

    if "!setidiom" in message:
        file = FileManager(filename="english_idioms_data.json")
        file.updating_json(message.text)

    if "!setlanguage" in message:
        new_language = message.text.split()[1]
        if new_language in languages:
            database.updating_user_translation(user_id=user_id, translation="en")
            database.updating_user_language(user_id=user_id, language=new_language)

    await bot.delete_message(chat_id, message_id)
