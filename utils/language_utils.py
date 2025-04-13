from config import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE
from locales.en import texts as en_texts
from locales.tr import texts as tr_texts
from locales.ru import texts as ru_texts
from locales.ar import texts as ar_texts

def get_text(key, language_code=DEFAULT_LANGUAGE):
    """Get text in the specified language."""
    if language_code not in SUPPORTED_LANGUAGES:
        language_code = DEFAULT_LANGUAGE
    
    texts = {
        'en': en_texts,
        'tr': tr_texts,
        'ru': ru_texts,
        'ar': ar_texts
    }
    
    language_texts = texts.get(language_code, en_texts)
    
    # Return the text or fallback to English if not found
    return language_texts.get(key, en_texts.get(key, f"Missing text: {key}"))
