from aiogram import Router
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import start_keyboard, guess_word_keyboard, default_menu
from aiogram.types import CallbackQuery
from games.games import Games
from filters.main_menu_filters import main_menu_filter
from aiogram.types import InputMediaPhoto, FSInputFile, BufferedInputFile, InputMediaAudio
import os
router = Router()


@router.callback_query(main_menu_filter)
async def process_main_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    gamer = Games(user_id, data="english_5k.json")
    file = gamer.game_data.base_pic
    database = gamer.database

    language = await database.checking_user_translation()

    if callback.data == "menu_button":
        await database.updating_user_game()
        keyboard = create_inline_kb(2, **start_keyboard)
        file_name = file
        file = FSInputFile(path=file_name)
        await callback.message.edit_media(media=InputMediaPhoto(media=file),
                                          text="Hello. Choose something", reply_markup=keyboard)

    if callback.data == "guess_word":
        keyboard = create_inline_kb(2, last_btn=default_menu, **guess_word_keyboard)
        file_name = file
        file = FSInputFile(path=file_name)
        await callback.message.edit_media(media=InputMediaPhoto(media=file), text="Choose parts of speech",
                                          reply_markup=keyboard)

    if callback.data == "word_constructor":
        await database.updating_user_answer()
        question, variants, audio = await gamer.word_constructor()
        keyboard = create_inline_kb(3, default_menu, *variants)
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file, caption=f"'{question}'"),
                                          reply_markup=keyboard)

    if callback.data == "/v":
        await database.updating_user_game(game="v")
        await database.updating_user_answer()
        variants, question, audio = await gamer.constructor_phrases(language=language)
        keyboard = create_inline_kb(2, default_menu, *variants)
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file, caption=f"'{question}'"),
                                          reply_markup=keyboard)

    await callback.answer()
