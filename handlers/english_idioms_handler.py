from aiogram import Router
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import default_menu, english_idioms_keyboard
from aiogram.types import CallbackQuery
from games.games import Games
from filters.english_idioms_filter import english_idioms_filter
from useful_functuons.functions import replacer_escaped_symbols
from aiogram.types import InputMediaAudio, BufferedInputFile
from useful_functuons.text_converter import converting_text_to_audio

router = Router()


@router.callback_query(english_idioms_filter)
async def process_english_idioms(callback: CallbackQuery):
    user_id = callback.from_user.id
    gamer = Games(user_id, data="english_idioms_data.json")

    if callback.data == "/idioms":
        key, values = gamer.game_data.getting_random_object_from_json()
        should_be_escaped = gamer.getting_context(word=key)
        should_be_escaped = list(should_be_escaped)
        should_be_escaped.append(values)
        should_be_escaped = replacer_escaped_symbols(should_be_escaped)
        context, translation, values = should_be_escaped
        text_audio = key
        audio = converting_text_to_audio(text_audio)
        text = f" ***{key}***  \n\n{values} \n\n{context} \n\n{translation}"
        keyboard = create_inline_kb(2, last_btn=default_menu, **english_idioms_keyboard)
        file = BufferedInputFile(file=audio, filename=str(user_id))
        await callback.message.edit_media(media=InputMediaAudio(media=file,
                                                                caption=text, parse_mode="MarkdownV2"),
                                          reply_markup=keyboard)
    await callback.answer()
