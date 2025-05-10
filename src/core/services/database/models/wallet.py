from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Numeric

from src.core.services.database.models.base import Base, int_pk


class WalletModel(Base):
    __tablename__ = "wallets"
    
    user_id:Mapped[int_pk]
    currency:Mapped[str] = mapped_column(String, index=True)
    balance:Mapped[float] = mapped_column(Numeric(36, 18), default=0)
    locked:Mapped[float] = mapped_column(Numeric(36, 18), default=0)