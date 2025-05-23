from sqlalchemy import String, Numeric
from sqlalchemy.orm import mapped_column, Mapped

from src.core.services.database.models.base import Base, int_pk, updated_at


class TokenModel(Base):
    __tablename__ = "tokens"
    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(64))
    symbol: Mapped[str] = mapped_column(String(16))
    price: Mapped[float] = mapped_column(Numeric)
    last_updated: Mapped[updated_at]