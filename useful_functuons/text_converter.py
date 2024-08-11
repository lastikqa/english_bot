import io
from gtts import gTTS
from english_bot_database.english_bot_database import EnglishBotDatabase


def converting_text_to_audio(text: str):
    audio = gTTS(text=text, lang="en", slow=False)
    audio_bytes = io.BytesIO()
    audio.write_to_fp(audio_bytes)
    return audio_bytes.getvalue()



