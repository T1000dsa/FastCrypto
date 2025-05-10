from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import func
from typing import Annotated
from datetime import datetime


class Base(DeclarativeBase):pass

int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime, 
    mapped_column(server_default=func.timezone('UTC', func.now()))
]
updated_at = Annotated[
    datetime, 
    mapped_column(
        server_default=func.timezone('UTC', func.now()),
        onupdate=func.timezone('UTC', func.now())
    )
]