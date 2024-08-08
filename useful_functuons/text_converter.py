import io
from gtts import gTTS
from english_bot_database.english_bot_database import EnglishBotDatabase


def converting_text_to_audio(text: str):
    audio = gTTS(text=text, lang="en", slow=False)
    audio_bytes = io.BytesIO()
    audio.write_to_fp(audio_bytes)
    return audio_bytes.getvalue()


def giving_audio(user_id: int):

    user_translation = EnglishBotDatabase(user_id).checking_user_translation(user_id)
    if user_translation == "en":
        word = EnglishBotDatabase(user_id).checking_answer(user_id)
    else:
        word = EnglishBotDatabase(user_id).checking_question(user_id)
    audio_bytes = converting_text_to_audio(word)
    EnglishBotDatabase(user_id).updating_user_media_data(user_id, media=audio_bytes)
    return audio_bytes
