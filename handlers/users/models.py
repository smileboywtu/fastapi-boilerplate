# -*- coding: utf-8 -*-


"""

user orm

"""

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), comment='用户名')
    age: Mapped[int] = mapped_column(comment='年龄')
    address: Mapped[str] = mapped_column(String(30), comment='用户地址')
    mobile: Mapped[str] = mapped_column(String(11), comment='手机号')

    def __repr__(self) -> str:
        return self.username
