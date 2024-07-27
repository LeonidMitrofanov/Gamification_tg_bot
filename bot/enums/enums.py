from enum import Enum, auto


class UserRole(Enum):
    USER = 0
    ADMIN = 1


class Tribe(Enum):
    AQUA = 1
    IGNIS = 2
    # AIR = 3
    # TERRA = 4


class EventState(Enum):
    ON_REVIEW = 0
    APPROVED = 1
    REJECTED = 2
    IN_PROGRESS = 3
    COMPLETED = 4
