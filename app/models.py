from typing import Any

from sqlalchemy import JSON
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column)


class Base(DeclarativeBase):
    """
    Базовый класс для моделей.
    """

    __abstract__ = True
    type_annotation_map = {dict[str, Any]: JSON}

    @declared_attr.directive
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"


class Wallet(Base):
    """
    Модель кошелька.
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column()
    bandwidth: Mapped[int] = mapped_column()
    energy: Mapped[dict[str, Any]] = mapped_column()
    balance: Mapped[int] = mapped_column()
