from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    username:str
    password:str
    email:Optional[str] = None


"""
class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int_pk]
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    join_date: Mapped[created_at]
    last_time_login: Mapped[updated_at]
    is_active:Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
"""