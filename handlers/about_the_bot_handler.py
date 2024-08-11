from aiogram import Router
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import default_menu
from lexicon.user_handlers_lexicon import about_the_bot_keyboard, bot_commands, guess_words, constructor_games
from lexicon.user_handlers_lexicon import rating
from aiogram.types import CallbackQuery
from filters.filter_about_the_bot import about_the_bot_filter
from aiogram.types import InputMediaPhoto, FSInputFile
import os
router = Router()


@router.callback_query(about_the_bot_filter)
async def process_about_the_bot_menu(callback: CallbackQuery):

    main_picture = os.path.abspath('data\\english_5k.png')

    if callback.data == "/about_the_bot":
        keyboard = create_inline_kb(2, last_btn=default_menu, **about_the_bot_keyboard)
        file = FSInputFile(path=main_picture)
        await callback.message.edit_media(media=InputMediaPhoto(media=file, caption="Read carefully"),
                                          reply_markup=keyboard)

    elif callback.data == "/bot_commands":
        keyboard = create_inline_kb(1, last_btn=default_menu)
        file = FSInputFile(path=main_picture)
        await callback.message.edit_media(media=InputMediaPhoto(media=file, caption=bot_commands,
                                                                parse_mode="MarkdownV2"),
                                          reply_markup=keyboard)
    elif callback.data == "/guess_words":
        keyboard = create_inline_kb(1, last_btn=default_menu)
        file = FSInputFile(path=main_picture)
        await callback.message.edit_media(media=InputMediaPhoto(media=file, caption=guess_words,
                                                                parse_mode="MarkdownV2"),
                                          reply_markup=keyboard)

    elif callback.data == "/constructor_games":
        keyboard = create_inline_kb(1, last_btn=default_menu)
        file = FSInputFile(path=main_picture)
        await callback.message.edit_media(media=InputMediaPhoto(media=file, caption=constructor_games,
                                                                parse_mode="MarkdownV2"),
                                          reply_markup=keyboard)

    elif callback.data == "/rating":
        keyboard = create_inline_kb(1, last_btn=default_menu)
        file = FSInputFile(path=main_picture)
        await callback.message.edit_media(media=InputMediaPhoto(media=file, caption=rating,
                                                                parse_mode="MarkdownV2"),
                                          reply_markup=keyboard)
    await callback.answer()
