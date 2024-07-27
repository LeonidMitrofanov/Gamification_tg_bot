from typing import Optional


class DBUser:
    def __init__(self,
                 user_id: int,
                 tg_id: int,
                 tg_teg: str | None,
                 name: str,
                 tribe_id: int,
                 role_id: int,
                 wallet_token: int,
                 language: str,
                 description: str | None = None,
                 photo_path: str | None = None) -> None:
        self.user_id = user_id
        self.tg_id = tg_id
        self.tg_teg = tg_teg
        self.name = name
        self.tribe_id = tribe_id
        self.role_id = role_id
        self.wallet_token = wallet_token
        self.language = language
        self.description = description
        self.photo_path = photo_path

    def __repr__(self):
        return (f"DBUser(user_id={self.user_id}, tg_id={self.tg_id}, tg_teg='{self.tg_teg}', name='{self.name}', "
                f"tribe_id={self.tribe_id}, role_id={self.role_id}, wallet_token={self.wallet_token}, "
                f"language='{self.language}', description='{self.description}', photo_path='{self.photo_path}')")
