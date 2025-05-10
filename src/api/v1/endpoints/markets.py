from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio

from src.core.services.crypto.exchange.trade import OrderBook


router = APIRouter()

@router.websocket("/ws/orderbook/{market}")
async def websocket_orderbook(websocket: WebSocket, market: str):
    await websocket.accept()
    order_book = OrderBook(market)
    
    try:
        while True:
            # Send initial snapshot
            snapshot = order_book.get_snapshot()
            await websocket.send_json(snapshot)
            
            # Subscribe to updates
            # This would use a PubSub system in production
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass