from dataclasses import dataclass


@dataclass
class DBUser:
    user_id: int
    tg_id: int
    tg_teg: str | None
    name: str
    tribe_id: int
    role_id: int
    wallet_token: int
    language: str
    description: str | None
    photo_path: str | None
