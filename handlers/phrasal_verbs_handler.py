from aiogram import Router
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import default_menu, phrasal_verbs_keyboard
from aiogram.types import CallbackQuery
from games.games import Games
from filters.phrasal_verbs_filter import phrasal_verbs_filter
from useful_functuons.functions import replacer_escaped_symbols

router = Router()


@router.callback_query(phrasal_verbs_filter)
async def process_phrasal_verbs(callback: CallbackQuery):
    user_id = callback.from_user.id
    gamer = Games(user_id, data="phrasal_verbs.json")

    if callback.data == "phrasal_verbs":
        key, values = gamer.game_data.getting_random_object_from_json()
        should_be_escaped = gamer.getting_context(word=key)
        should_be_escaped = list(should_be_escaped)
        should_be_escaped.append(values[0])
        should_be_escaped = replacer_escaped_symbols(should_be_escaped)
        context, translation, values = should_be_escaped
        text = f" ***{key}***  \n\n{values} \n\n{context} \n\n{translation}"
        keyboard = create_inline_kb(2, last_btn=default_menu, **phrasal_verbs_keyboard)
        await callback.message.edit_text(text=text, parse_mode="MarkdownV2", reply_markup=keyboard)
    await callback.answer()
