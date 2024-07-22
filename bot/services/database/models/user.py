from typing import Optional


class DBUser:
    def __init__(self,
                 user_id: int,
                 tg_id: int,
                 name: str,
                 tribe_id: int,
                 role_id: int,
                 wallet_token: int,
                 description: str | None = None,
                 photo_path: str | None = None) -> None:
        self.user_id = user_id
        self.tg_id = tg_id
        self.name = name
        self.tribe_id = tribe_id
        self.role_id = role_id
        self.wallet_token = wallet_token
        self.description = description
        self.photo_path = photo_path

    def __repr__(self):
        return (f"DBUser(user_id={self.user_id}, tg_id={self.tg_id}, name='{self.name}', tribe_id={self.tribe_id}, "
                f"role_id={self.role_id}, wallet_token={self.wallet_token}, description='{self.description}', "
                f"photo_path='{self.photo_path}')")
