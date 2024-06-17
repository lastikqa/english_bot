from aiogram import Router
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import default_menu, chuck_keyboard
from aiogram.types import CallbackQuery
from games.games import Games
from english_bot_database.english_bot_database import EnglishBotDatabase
from filters.chuck_norris_filter import chuck_filter

router = Router()


@router.callback_query(chuck_filter)
async def process_main_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    database = EnglishBotDatabase(user_id=callback.from_user.id)
    user_param = database.checking_user_game(user_id)
    gamer = Games(user_id, user_param)
    answer = database.checking_answer(user_id)

    if callback.data == "/chuck":
        joke = gamer.getting_jokes(user_id)
        keyboard = create_inline_kb(2, last_btn=default_menu, **chuck_keyboard)
        await callback.message.edit_text(text=joke, reply_markup=keyboard)

    if callback.data == "/translation":
        translation = gamer.getting_translation(user_id)
        keyboard = create_inline_kb(2, last_btn=default_menu, **chuck_keyboard)
        await callback.message.edit_text(text=f"{answer}\n \n{translation}", reply_markup=keyboard)
