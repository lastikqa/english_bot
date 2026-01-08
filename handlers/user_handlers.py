from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import start_keyboard, default_menu
from lexicon.user_handlers_lexicon import languages
from english_bot_database.english_bot_database import EnglishBotDatabase
from aiogram import Router
from data.file_manager import FileManager
from aiogram.types import FSInputFile

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    message_id = message.message_id
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    user_id = message.from_user.id
    database = EnglishBotDatabase(user_id)

    if await database.looking_for_user_in_db() is False:
        await database.creating_object_user_in_db(first_name)
    keyboard = create_inline_kb(2, **start_keyboard)
    file = FileManager.base_pic
    print(file)
    file = FSInputFile(path = file)
    await message.answer_photo(photo=file,
                               caption="Hello. Choose something", reply_markup=keyboard)
    await message.bot.delete_message(chat_id, message_id)


@router.message()
async def menu_button(message: Message):
    """the function processes menu button"""
    user_id = message.from_user.id
    database = EnglishBotDatabase(user_id)
    message_id = message.message_id
    chat_id = message.chat.id


    if message.text == "/translation":
        translation = await database.checking_user_translation()
        language = await database.checking_user_language()

        translation, language = language, translation
        await database.updating_user_translation(translation=translation)
        await database.updating_user_language(language=language)

    elif "!setnicname" in message.text.split()[0].lower():
        nickname = message.text.split()[1]
        await database.updating_user_first_name( nickname=nickname)

    elif message.text == '/scores':
        text = await database.getting_user_scores()
        keyboard = create_inline_kb(1, last_btn=default_menu)
        await message.answer(text=text, parse_mode="MarkdownV2", reply_markup=keyboard)

    elif "!setidiom" in message.text:
        file = FileManager(filename="english_idioms_data.json")
        file.updating_json(message.text)

    elif "!setlanguage" in message.text:
        new_language = message.text.split()[-1]
        if new_language in languages:
            await database.updating_user_translation(translation="en")
            await database.updating_user_language(language=new_language)

    await message.bot.delete_message(chat_id, message_id)
