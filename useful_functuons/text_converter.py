import io
import asyncio
from gtts import gTTS


async def converting_text_to_audio(text: str):
    """Асинхронная конвертация текста в аудио"""
    # Запускаем синхронную функцию в отдельном потоке
    return await asyncio.to_thread(_convert_text_to_audio_sync, text)


def _convert_text_to_audio_sync(text: str):
    """Синхронная функция конвертации текста в аудио"""
    audio = gTTS(text=text, lang="en", slow=False)
    audio_bytes = io.BytesIO()
    audio.write_to_fp(audio_bytes)
    return audio_bytes.getvalue()
