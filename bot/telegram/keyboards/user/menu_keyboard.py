import logging
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.telegram.keyboards import keyboards_config
from bot.utils.xml_loader import get_message

logger = logging.getLogger(__name__)


def get_menu_keyboard(locale: str) -> ReplyKeyboardMarkup:
    """
    Create the main keyboard with localized button texts.

    :param locale: The language of the messages (e.g., 'en' for English, 'ru' for Russian).
    :return: ReplyKeyboardMarkup object with localized buttons.
    """
    logger.debug(f"Creating main keyboard with locale '{locale}'")
    try:
        profile_text = get_message('profile', locale, keyboards_config.menu_keyboard_buttons)
        events_text = get_message('events', locale, keyboards_config.menu_keyboard_buttons)
        store_text = get_message('store', locale, keyboards_config.menu_keyboard_buttons)
        support_text = get_message('support', locale, keyboards_config.menu_keyboard_buttons)
        search_participants_text = get_message('search_participants', locale, keyboards_config.menu_keyboard_buttons)
    except KeyError as e:
        logger.error(f"Error getting localized text: {e}")
        raise

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=profile_text), KeyboardButton(text=events_text)],
            [KeyboardButton(text=store_text), KeyboardButton(text=support_text)],
            [KeyboardButton(text=search_participants_text)]
        ],
        resize_keyboard=True
    )
