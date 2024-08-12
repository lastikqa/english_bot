from aiogram import Router
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import default_menu
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from games.games import Games
from filters.constructor_phrases_filter import constructor_phrases_filter
from aiogram.types import InputMediaAudio, BufferedInputFile
router = Router()


@router.callback_query(constructor_phrases_filter)
async def process_main_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    gamer = Games(user_id, data="english_5k.json")
    database = gamer.database
    user_question = database.checking_question()
    user_variants = database.checking_user_variants()
    variants = database.checking_variants_for_user()
    game_status = database.checking_user_game()
    language = database.checking_user_translation()
    audio = database.getting_user_media_data()

    if game_status == "v" and callback.data in user_variants:
        try:
            user_variants.remove(callback.data)
            database.updating_user_variants(user_variants)
            user_answer = (database.checking_user_answer()+" "+callback.data)
            database.updating_user_answer(user_answer=user_answer)
            user = database.checking_user_variants()
            user_ans = database.checking_user_answer()
            keyboard = create_inline_kb(2, default_menu, *user)
            file = BufferedInputFile(file=audio, filename=str(user_id))
            await callback.message.edit_media(media=InputMediaAudio(media=file,
                                                                    caption=f"{user_question} \n{user_ans}"),
                                              reply_markup=keyboard)
        except TelegramBadRequest:
            user_answer = database.checking_user_answer().strip()
            answer = database.checking_answer()
            if user_answer == answer and len(user_variants) == 0:
                database.updating_user_answer()
                win = (database.checking_counter_user_score()) + 1
                database.updating_score_count(win=win)
                variants, question, audio = await gamer.constructor_phrases(language=language)
                keyboard = create_inline_kb(2, default_menu, *variants)
                file = BufferedInputFile(file=audio, filename=str(user_id))
                await callback.message.edit_media(media=InputMediaAudio(media=file, caption=f"'{question}'"),
                                                  reply_markup=keyboard)
            else:
                database.updating_user_answer()
                user_score = database.checking_user_score()
                counter_user_score = database.checking_counter_user_score()
                database.updating_user_variants(variants)
                if counter_user_score > user_score:
                    database.updating_user_score(counter=counter_user_score)
                database.updating_score_count()
                keyboard = create_inline_kb(2, default_menu, *variants)
                file = BufferedInputFile(file=audio, filename=str(user_id))
                await callback.message.edit_media(media=InputMediaAudio(media=file, caption=f"'{user_question}'"),
                                                  reply_markup=keyboard)
    await callback.answer()
