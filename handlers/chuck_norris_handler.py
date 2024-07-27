from aiogram import Router
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import default_menu, chuck_keyboard
from aiogram.types import CallbackQuery
from games.games import Games
from english_bot_database.english_bot_database import EnglishBotDatabase
from filters.chuck_norris_filter import chuck_filter
import translators as ts
router = Router()


@router.callback_query(chuck_filter)
async def process_main_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    gamer = Games(user_id, data="english_5k.json")


    if callback.data == "/chuck":
        joke = gamer.getting_jokes(user_id)
        keyboard = create_inline_kb(2, last_btn=default_menu, **chuck_keyboard)
        await callback.message.edit_text(text=joke, reply_markup=keyboard)

    if callback.data == "/translation":
        database = EnglishBotDatabase(user_id)
        answer = database.checking_answer(user_id)
        translation = gamer.getting_absolute_translation()
        translated = ts.translate_text(answer, to_language=translation)
        keyboard = create_inline_kb(2, last_btn=default_menu, **chuck_keyboard)
        await callback.message.edit_text(text=f"{answer}\n \n{translated}", reply_markup=keyboard)
