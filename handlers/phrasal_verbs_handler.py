from aiogram import Router
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import default_menu, phrasal_verbs_keyboard
from aiogram.types import CallbackQuery
from games.games import Games
from english_bot_database.english_bot_database import EnglishBotDatabase
from data.phrasal_verbs import phrasal_verbs
from data.phrasal_verbs_key_list import phrasal_verbs_key_list
from filters.phrasal_verbs_filter import phrasal_verbs_filter
from useful_functuons.functions import replacer_escaped_symbols

router = Router()


@router.callback_query(phrasal_verbs_filter)
async def process_phrasal_verbs(callback: CallbackQuery):
    user_id = callback.from_user.id
    database = EnglishBotDatabase(user_id=callback.from_user.id)
    user_param = database.checking_user_game(user_id)
    gamer = Games(user_id, user_param)

    if callback.data == "phrasal_verbs":
        key, values = gamer.getting_dictionaries_data(dictionary=phrasal_verbs, key_list=phrasal_verbs_key_list)
        should_be_escaped = gamer.getting_context(word=key)
        should_be_escaped = list(should_be_escaped)
        should_be_escaped.append(values[0])
        should_be_escaped = replacer_escaped_symbols(should_be_escaped)
        context, translation, values = should_be_escaped
        text = f" ***{key}***  \n\n{values} \n\n{context} \n\n{translation}"
        keyboard = create_inline_kb(2, last_btn=default_menu, **phrasal_verbs_keyboard)
        await callback.message.edit_text(text=text, parse_mode="MarkdownV2", reply_markup=keyboard)
    await callback.answer()
