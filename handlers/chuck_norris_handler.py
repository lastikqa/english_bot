from aiogram import Router
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import default_menu, chuck_keyboard
from aiogram.types import CallbackQuery
from games.games import Games
from filters.chuck_norris_filter import chuck_filter
from useful_functuons.translation import translation_text
from aiogram.types import BufferedInputFile, InputMediaAudio

router = Router()


@router.callback_query(chuck_filter)
async def process_main_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    gamer = Games(user_id, data="english_5k.json")
    database = gamer.database

    if callback.data == "/chuck":
        joke = await gamer.getting_jokes()
        joke = joke["joke"]
        await gamer.database.updating_answer(joke)
        audio = await gamer.giving_audio()
        keyboard = create_inline_kb(2, last_btn=default_menu, **chuck_keyboard)
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file, caption=f"'{joke}'"),
                                          reply_markup=keyboard)

    if callback.data == "/translation":
        answer = await database.checking_answer()
        translation = await gamer.getting_absolute_translation()
        translated = translation_text(answer, to_language=translation)
        keyboard = create_inline_kb(2, last_btn=default_menu, **chuck_keyboard)
        audio = await database.getting_user_media_data()
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file, caption=f"{answer}\n \n{translated}"),
                                          reply_markup=keyboard)
