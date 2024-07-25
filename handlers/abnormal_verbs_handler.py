from aiogram import Router
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon import default_menu, abnormal_verbs_keyboard
from aiogram.types import CallbackQuery
from games.games import Games
from filters.abnormal_verbs_filter import abnormal_verbs_filter
from useful_functuons.functions import replacer_escaped_symbols


router = Router()


@router.callback_query(abnormal_verbs_filter)
async def process_abnormal_verbs(callback: CallbackQuery):
    user_id = callback.from_user.id
    gamer = Games(user_id, data="abnormal_verbs.json")

    if callback.data == "abnormal_verbs":

        key, values = gamer.game_data.getting_random_object_from_json()
        sentences = gamer.getting_context(values[0])
        sentences = replacer_escaped_symbols(list(sentences))

        text = (f"\\    ***{values[3].title()}*** \n\n\\* ***Base Form***   {key} "
                f"\n\n\\* ***Past Form***   {values[1]} \n\n"
                f"\\* ***Participle***   {values[2]} \n\n{sentences[0]} \n\n{sentences[1]}")
        keyboard = create_inline_kb(2, last_btn=default_menu, **abnormal_verbs_keyboard)
        await callback.message.edit_text(text=text, parse_mode="MarkdownV2", reply_markup=keyboard)
    await callback.answer()
