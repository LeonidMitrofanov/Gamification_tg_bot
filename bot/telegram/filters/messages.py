from aiogram import F

from bot.enums.language import Language
from bot.utils.xml_loader import get_message


def contains_message_on_any_language(key: str, messages: dict[str, dict[str, str]]) -> F:
    def check_message(text: str) -> bool:
        for lang in Language.ALL:
            message = get_message(key, lang, messages)
            if message in text:
                return True
        return False

    return F.text.func(check_message)
