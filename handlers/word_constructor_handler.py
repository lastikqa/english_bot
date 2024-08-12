from aiogram import Router
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import default_menu
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from games.games import Games
from filters.word_constructor_filter import word_constructor_filter
from aiogram.types import BufferedInputFile, InputMediaAudio

router = Router()


@router.callback_query(word_constructor_filter)
async def processing_word_constructors(callback: CallbackQuery):
    user_id = callback.from_user.id
    gamer = Games(user_id, data="english_5k.json")
    database = gamer.database

    user_question = await database.checking_question()
    user_variants = await database.checking_user_variants()
    variants = await database.checking_variants_for_user()
    game_status = await database.checking_user_game()
    audio = await database.getting_user_media_data()

    if game_status == "word_constructor" and callback.data in user_variants:
        try:
            user_variants.remove(callback.data)
            await database.updating_user_variants(user_variants)
            if callback.data == "_":
                data = " "
                user_answer = (await database.checking_user_answer() + data)
            else:
                user_answer = (await database.checking_user_answer() + callback.data)
            await database.updating_user_answer(user_answer=user_answer)
            user_variants = await database.checking_user_variants()
            keyboard = create_inline_kb(3, default_menu, *user_variants)
            file = BufferedInputFile(file=audio, filename=str(user_id))
            await callback.message.edit_media(media=InputMediaAudio(media=file,
                                                                    caption=f"{user_question} \n{user_answer} "),
                                              reply_markup=keyboard)
        except TelegramBadRequest:
            user_answer = await database.checking_user_answer()
            user_answer = user_answer.strip()
            answer = await database.checking_answer()
            if user_answer == answer:
                await database.updating_user_answer()
                await database.updating_user_rating()
                question, variants, audio = await gamer.word_constructor()
                keyboard = create_inline_kb(3, default_menu, *variants)
                file = BufferedInputFile(file=audio, filename=str(user_id))
                await callback.message.edit_media(media=InputMediaAudio(media=file, caption=f"'{question}'"),
                                                  reply_markup=keyboard)
            else:
                await database.updating_user_answer()
                await database.updating_user_variants(variants)
                await database.updating_user_rating(win=False)
                keyboard = create_inline_kb(3, default_menu, *variants)
                file = BufferedInputFile(file=audio, filename=str(user_id))
                await callback.message.edit_media(media=InputMediaAudio(media=file, caption=f"'{user_question}'"),
                                                  reply_markup=keyboard)

    await callback.answer()
