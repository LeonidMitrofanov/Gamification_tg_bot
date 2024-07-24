import xml.etree.ElementTree as ET
import logging
import os

# Configure logger
logger = logging.getLogger(__name__)


def load_messages_from_xml(file_path: str) -> dict[str, dict[str, str]]:
    """
    Load messages from an XML file and return them as a dictionary.

    :param file_path: Path to the XML file.
    :return: Dictionary of messages keyed by their message key and locale.
    """
    logger.debug(f"Starting load_messages_from_xml function from '{file_path}'")

    if not os.path.exists(file_path):
        logger.error(f"XML file {file_path} not found.")
        raise FileNotFoundError(f"XML file {file_path} not found.")

    messages = {}
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Iterate through message elements
        for message_elem in root.findall('message'):
            key = message_elem.get('id')
            if not key:
                logger.warning(f"Message without 'id' found.")
                continue

            locales = {}
            for text_elem in message_elem.findall('text'):
                lang = text_elem.get('lang')
                text = text_elem.text
                if lang and text:
                    locales[lang] = text
                else:
                    logger.warning(f"Text element missing 'lang' or text content.")

            if locales:
                messages[key] = locales
            else:
                logger.warning(f"No locales found for message key '{key}'.")

        logger.info(f"Messages loaded successfully from {file_path}")
    except ET.ParseError as e:
        logger.error(f"Error parsing XML file {file_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading messages from XML file {file_path}: {e}")
        raise

    return messages


def get_message(key: str, locale: str, messages: dict[str, dict[str, str]]) -> str:
    """
    Returns the message for the given key and locale.

    :param key: The key to retrieve the message from the messages dictionary (e.g., 'welcome_user').
    :param locale: The language of the message (e.g., 'en' for English, 'ru' for Russian).
    :param messages: The dictionary containing all the messages.
    :return: The message in the specified language.
    :raises KeyError: If the key or locale is not found in the messages' dictionary.
    """
    logger.debug(f"Starting get_message function with key: '{key}' and locale: '{locale}'")

    # Retrieve the dictionary of messages for the given key
    message_dict = messages.get(key)
    if message_dict is None:
        logger.error(f"Message key '{key}' not found.")
        raise KeyError(f"Message key '{key}' not found.")

    # Retrieve the message in the specified locale
    message = message_dict.get(locale)
    if message is None:
        logger.error(f"Locale '{locale}' not found for message key '{key}'.")
        raise KeyError(f"Locale '{locale}' not found for message key '{key}'.")

    return message


