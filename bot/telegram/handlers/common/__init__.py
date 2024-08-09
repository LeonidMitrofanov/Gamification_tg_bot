from typing import Final
from aiogram import Router

from . import menu, registration, profile

router: Final[Router] = Router(name=__name__)
router.include_routers(registration.router, menu.router, profile.router)
