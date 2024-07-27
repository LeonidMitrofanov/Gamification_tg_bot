import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from bot.enums.language import Language
from bot.telegram.handlers import handlers_config as config
from bot.states.registration import RegistrationStates
from bot.services.database.response import user as db_user
from bot.utils.json_loader import get_message

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} initiated registration.")

    user_id = message.from_user.id
    if await db_user.user_exists(tg_id=user_id):
        user = await db_user.get_user(tg_id=user_id)
        username = message.from_user.username
        await db_user.update_user_tg_teg(user_id, username)
        welcome_message = get_message('welcome_user', Language.DEFAULT, config.menu_messages)
        await message.answer(welcome_message.format(first_name=user.name))
        await message.answer(get_message('update_tag', Language.DEFAULT, config.menu_messages))
    else:
        await message.answer(
            get_message('enter_secret_phrase', Language.DEFAULT, config.registration_messages))
        await state.set_state(RegistrationStates.waiting_for_secret_phrase)


@router.message(StateFilter(RegistrationStates.waiting_for_secret_phrase))
async def enter_secret_phrase(message: types.Message, state: FSMContext):
    logger.debug(f"User {message.from_user.id} entered secret phrase.")
    if message.text == config.USER_SECRETKEY:
        await state.update_data(user_role='user')
        await message.answer(get_message('enter_surname', Language.DEFAULT, config.registration_messages))
        await state.set_state(RegistrationStates.waiting_for_surname)
    elif message.text == config.ADMIN_SECRETKEY:
        await state.update_data(user_role='admin')
        await message.answer(get_message('enter_surname', Language.DEFAULT, config.registration_messages))
        await state.set_state(RegistrationStates.waiting_for_surname)
    else:
        await message.answer(get_message('invalid_secret_phrase',
                                         Language.DEFAULT,
                                         config.registration_messages))


@router.message(StateFilter(RegistrationStates.waiting_for_surname))
async def enter_surname(message: types.Message, state: FSMContext):
    logger.debug(f"User {message.from_user.id} entered surname.")
    if message.text.isalpha():
        await state.update_data(surname=message.text)
        await message.answer(get_message('enter_name', Language.DEFAULT, config.registration_messages))
        await state.set_state(RegistrationStates.waiting_for_name)
    else:
        await message.answer(get_message('invalid_surname', Language.DEFAULT, config.registration_messages))


@router.message(StateFilter(RegistrationStates.waiting_for_name))
async def enter_name(message: types.Message, state: FSMContext):
    logger.debug(f"User {message.from_user.id} entered name.")
    if message.text.isalpha():
        user_data = await state.get_data()
        surname = user_data.get('surname')
        name = message.text
        username = f"{surname} {name}"
        user_role = user_data.get('user_role')

        if user_role == 'admin':
            await db_user.add_admin(tg_id=message.from_user.id, name=username,
                                    language=message.from_user.language_code)
            await message.answer(
                get_message('registration_successful', Language.DEFAULT, config.registration_messages))
        else:
            await db_user.add_user(tg_id=message.from_user.id, name=username,
                                   language=message.from_user.language_code)
            await message.answer(get_message('registration_successful',
                                             Language.DEFAULT, config.registration_messages))

        await state.clear()
    else:
        await message.answer(get_message('invalid_name', Language.DEFAULT, config.registration_messages))

# @router.message(Command("start"))
# async def start_command(message: types.Message, bot: Bot):
#     user_id = message.from_user.id
#     user = await db_user.get_user(tg_id=user_id)
#     username = '@' + message.from_user.username
#     first_name = message.from_user.first_name
#     logger.debug(f"Received /start command from user_id: {user_id}, username: {username}")
#
#     try:
#         if await db_user.user_exists(tg_id=user_id):
#             await db_user.update_user_tg_teg(user_id, username)
#             await message.answer(get_message('welcome_user', user.language, messages).format(first_name=user.name))
#             await message.answer(get_message('update_tag', user.language, messages))
#         else:
#             logger.warning(f"User with tg_id: {user_id} not found in the database")
#             await message.answer(get_message('not_registered', user.language, messages))
#     except Exception as e:
#         logger.exception(f"Error processing /start command for user_id: {user_id}: {e}")
#         await message.answer(get_message("start_error", user.language, messages))
