import translators as ts
from config import translator


def translation_text(text: str, to_language):
    translated = ts.translate_text(text, to_language=to_language, translator=translator)
    return translated
