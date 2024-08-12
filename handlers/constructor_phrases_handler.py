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
    user_question = await database.checking_question()
    user_variants = await database.checking_user_variants()
    variants = await database.checking_variants_for_user()
    game_status = await database.checking_user_game()
    language = await database.checking_user_translation()
    audio = await database.getting_user_media_data()

    if game_status == "v" and callback.data in user_variants:
        try:
            user_variants.remove(callback.data)
            await database.updating_user_variants(user_variants)
            user_answer = (await database.checking_user_answer()+" "+callback.data)
            await database.updating_user_answer(user_answer=user_answer)
            user = await database.checking_user_variants()
            user_ans = await database.checking_user_answer()
            keyboard = create_inline_kb(2, default_menu, *user)
            file = BufferedInputFile(file=audio, filename=str(user_id))
            await callback.message.edit_media(media=InputMediaAudio(media=file,
                                                                    caption=f"{user_question} \n{user_ans}"),
                                              reply_markup=keyboard)
        except TelegramBadRequest:
            user_answer = await database.checking_user_answer()
            user_answer = user_answer.strip()
            answer = await database.checking_answer()
            if user_answer == answer and len(user_variants) == 0:
                await database.updating_user_answer()
                win = (await database.checking_counter_user_score()) + 1
                await database.updating_score_count(win=win)
                variants, question, audio = await gamer.constructor_phrases(language=language)
                keyboard = create_inline_kb(2, default_menu, *variants)
                file = BufferedInputFile(file=audio, filename=str(user_id))
                await callback.message.edit_media(media=InputMediaAudio(media=file, caption=f"'{question}'"),
                                                  reply_markup=keyboard)
            else:
                await database.updating_user_answer()
                user_score = await database.checking_user_score()
                counter_user_score = await database.checking_counter_user_score()
                await database.updating_user_variants(variants)
                if counter_user_score > user_score:
                    await database.updating_user_score(counter=counter_user_score)
                await database.updating_score_count()
                keyboard = create_inline_kb(2, default_menu, *variants)
                file = BufferedInputFile(file=audio, filename=str(user_id))
                await callback.message.edit_media(media=InputMediaAudio(media=file, caption=f"'{user_question}'"),
                                                  reply_markup=keyboard)
    await callback.answer()
