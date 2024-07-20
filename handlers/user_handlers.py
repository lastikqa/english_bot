from aiogram import Bot
import time
from config import token
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import start_keyboard, help_message, default_menu
from english_bot_database.english_bot_database import EnglishBotDatabase
from aiogram import Router

router = Router()
time.sleep(5)
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
    database = EnglishBotDatabase(message.from_user.id)
    message_id = message.message_id
    chat_id = message.chat.id
    if message.text == "/help":
        keyboard = create_inline_kb(1, last_btn=default_menu)
        await message.answer(text=help_message, parse_mode="MarkdownV2", reply_markup=keyboard)

    if message.text == "/translation":
        translation = database.checking_user_translation(user_id=message.from_user.id)
        database.updating_user_translation(translation=translation, user_id=message.from_user.id)

    if "!set" in message.text.split()[0].lower():
        nickname = message.text.split()[1]
        database.updating_user_first_name(user_id=message.from_user.id, nickname=nickname)

    if message.text == '/scores':
        user_rating, user_score  = database.getting_user_scores(user_id= message.from_user.id)
        keyboard = create_inline_kb(1, last_btn=default_menu)
        text = "User Rating"
        for i in user_rating:
            text += "\n" + i[0] + " " + str(i[1])
        text += "\n" + user_score[0]+ " " + str(user_score[-1]) + "\n"

        await message.answer(text=text, parse_mode="MarkdownV2", reply_markup=keyboard)
    await bot.delete_message(chat_id, message_id)
