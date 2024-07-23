from aiogram import Router
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import default_menu, english_idioms_keyboard
from aiogram.types import CallbackQuery
from games.games import Games
from english_bot_database.english_bot_database import EnglishBotDatabase
from data.file_manager import FileManager
from filters.english_idioms_filter import english_idioms_filter
from useful_functuons.functions import replacer_escaped_symbols


router = Router()


@router.callback_query(english_idioms_filter)
async def process_english_idioms(callback: CallbackQuery):
    user_id = callback.from_user.id
    database = EnglishBotDatabase(user_id=callback.from_user.id)
    user_param = database.checking_user_game(user_id)
    gamer = Games(user_id, user_param)
    filename = "english_idioms_data.json"
    file = FileManager(filename)

    if callback.data == "/idioms":
        key, values = file.getting_random_object_from_json()
        should_be_escaped = gamer.getting_context(word=key)
        should_be_escaped = list(should_be_escaped)
        should_be_escaped.append(values)
        should_be_escaped = replacer_escaped_symbols(should_be_escaped)
        context, translation, values = should_be_escaped
        text = f" ***{key}***  \n\n{values} \n\n{context} \n\n{translation}"
        keyboard = create_inline_kb(2, last_btn=default_menu, **english_idioms_keyboard)
        await callback.message.edit_text(text=text, parse_mode="MarkdownV2", reply_markup=keyboard)
    await callback.answer()
