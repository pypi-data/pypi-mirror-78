from typing import cast

from news_mining_db.models.base_model import Base
from sqlalchemy import Column, Integer, String, Boolean
from hashlib import sha256


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)

    password_hashed = Column(String(64), nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    email = Column(String(32), nullable=False, unique=True)

    is_staff = Column(Boolean, server_default='f', nullable=False)

    @property
    def password(self):
        return self.password_hashed

    @password.setter
    def password(self, value: str):
        self.password_hashed = sha256(bytes(value, 'utf-8')).hexdigest()

    def is_password_correct(self, password: str) -> bool:
        return self.password_hashed == sha256(bytes(password, 'utf-8')).hexdigest()

    @classmethod
    def upsert(cls, *, username: str, email: str, password: str, is_staff: bool = False) -> "User":
        values = dict(
            username=username,
            email=email,
            password_hashed=sha256(bytes(password, 'utf-8')).hexdigest(),
            is_staff=is_staff,
        )

        values = {key: value for key, value in values.items() if value is not None}

        user = cast(
            "User",
            cls.upsert_row(
                row_class=cls,
                index_elements=["email"],
                set_=values,
                values=values,
            ),
        )

        return user
