from sqlalchemy import String, Numeric, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped

from src.core.services.database.models.base import Base, int_pk

class OrderModel(Base):
    __tablename__ = "orders"
    
    id: Mapped[int_pk] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    market: Mapped[str] = mapped_column(String)
    side: Mapped[str] = mapped_column(Enum("buy", "sell", name="order_side"))
    type: Mapped[str] = mapped_column(Enum("limit", "market", name="order_type"))
    price: Mapped[float] = mapped_column(Numeric(36, 18))
    amount: Mapped[float] = mapped_column(Numeric(36, 18))
    filled: Mapped[float] = mapped_column(Numeric(36, 18), default=0)
    status: Mapped[str] = mapped_column(Enum("open", "filled", "canceled", name="order_status"))
    created_at: Mapped[DateTime] = mapped_column(DateTime)
    updated_at: Mapped[DateTime] = mapped_column(DateTime)