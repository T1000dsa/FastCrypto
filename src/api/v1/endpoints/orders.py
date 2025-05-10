from fastapi import APIRouter, Depends, Security
from fastapi.security import APIKeyHeader

from src.core.dependencies.db_helper import DBDI
from src.core.pydantic_schemas.trading_schema import OrderCreate
from src.core.dependencies.auth_deps import GET_CURRENT_ACTIVE_USER
from src.core.services.crypto.exchange.trade import OrderBook


api_key_header = APIKeyHeader(name="X-TRADING-API-KEY")

router = APIRouter(prefix="/orders")

@router.post("/", dependencies=[Security(api_key_header)])
async def create_order(
    order: OrderCreate,
    user: GET_CURRENT_ACTIVE_USER,
    db: DBDI
):
    current_user = OrderBook()
    return await current_user.create_order(user.id, order)