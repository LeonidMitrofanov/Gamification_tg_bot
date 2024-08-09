import logging
import os
from aiogram import Router, types
from aiogram.types import FSInputFile

from bot.enums.language import Language
from bot.telegram.handlers import handlers_config as config
from bot.telegram.keyboards import keyboards_config
from bot.telegram.filters.messages import contains_message_on_any_language
from bot.services.database.response import user as db_user
from bot.services.database.response import tribe as db_tribe
from bot.services.database.response import wallet
from bot.utils.xml_loader import get_message

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(contains_message_on_any_language("profile", keyboards_config.menu_keyboard_buttons))
async def get_self_profile(message: types.Message):
    await get_profile(message, message.from_user.id)


async def get_profile(message: types.Message, user_id: int):
    if await db_user.user_exists(tg_id=user_id):
        logger.debug(f"User {user_id} open profile.")
        user = await db_user.get_user(tg_id=user_id)
        profile = get_message('profile', user.language, config.profile_format)
        profile = profile.format(
            tg_teg=user.tg_teg,
            name=user.name,
            tribe_name=(await db_tribe.get_tribe(user.tribe_id)).tribe_name,
            position="get_tribe_position",  # TODO: get user position in tribe
            balance=await wallet.get_balance(user.wallet_token),
            description="" if user.description is None else user.description
        )

        # Check if photo_path is available, else use Telegram profile photo
        photo_path = user.photo_path
        if photo_path and os.path.exists(photo_path):
            try:
                # Create an InputFile object to send the photo
                photo = FSInputFile(photo_path, filename=f"{user.name}_profile_photo")
                await message.answer_photo(photo=photo, caption=profile, parse_mode='HTML')
            except Exception as e:
                logger.error(f"Error sending photo from path: {e}")
                await message.answer(profile, parse_mode='HTML')
        else:
            try:
                # Fallback to using the user's Telegram profile photo
                user_photos = await message.bot.get_user_profile_photos(user_id=user_id)
                if user_photos.total_count > 0:
                    photo_file_id = user_photos.photos[0][0].file_id
                    await message.answer_photo(photo=photo_file_id, caption=profile, parse_mode='HTML')
                else:
                    await message.answer(profile, parse_mode='HTML')
            except Exception as e:
                logger.error(f"Error fetching or sending Telegram profile photo: {e}")
                await message.answer(profile, parse_mode='HTML')
    else:
        await message.answer(get_message('profile_not_found', Language.DEFAULT, config.profile_format))
