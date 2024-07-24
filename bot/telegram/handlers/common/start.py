import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram import Bot

from bot.services.database.response import user as db_user
from bot.utils.json_loader import get_message
from bot.enums.language import Language

router = Router(name=__name__)
logger = logging.getLogger(__name__)
messages: dict[str, dict[str, str]]


@router.message(Command("start"))
async def start_command(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    username = '@' + message.from_user.username
    first_name = message.from_user.first_name
    logger.debug(f"Received /start command from user_id: {user_id}, username: {username}")

    try:
        if await db_user.user_exists(tg_id=user_id):
            await db_user.update_user_tg_teg(user_id, username)
            await message.answer(get_message('welcome_user', Language.DEFAULT, messages).format(first_name=first_name))
            await message.answer(get_message('update_tag', Language.DEFAULT, messages))
        else:
            logger.warning(f"User with tg_id: {user_id} not found in the database")
            await message.answer(get_message('not_registered', Language.DEFAULT, messages))
    except Exception as e:
        logger.exception(f"Error processing /start command for user_id: {user_id}: {e}")
        await message.answer(get_message("start_error", Language.RU, messages))
