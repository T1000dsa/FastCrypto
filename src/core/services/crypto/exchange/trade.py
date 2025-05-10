from sqlalchemy.ext.asyncio import AsyncSession
from collections import defaultdict
from sortedcontainers import SortedDict
from dataclasses import dataclass
from typing import Optional
import uuid

@dataclass
class Order:
    id: str
    user_id: int
    side: str  # 'buy' or 'sell'
    type: str  # 'limit', 'market'
    price: float
    amount: float
    filled: float = 0.0
    status: str = 'open'  # 'open', 'filled', 'canceled'

class OrderBook:
    def __init__(self):
        self.bids = SortedDict(lambda x: -x)  # Highest bid first
        self.asks = SortedDict()              # Lowest ask first
        self.orders = {}                      # OrderID -> Order
        self.user_orders = defaultdict(list)  # UserID -> List[OrderID]

    async def create_order(
        self,
        user_id: int,
        side: str,
        order_type: str,
        price: float,
        amount: float,
        **kwargs
    ) -> Order:
        """Main order creation endpoint"""
        order_id = str(uuid.uuid4())
        order = Order(
            id=order_id,
            user_id=user_id,
            side=side,
            type=order_type,
            price=price,
            amount=amount
        )
        
        # Validate order
        if not await self._validate_order(order):
            raise ValueError("Invalid order parameters")
        
        # Add to order book
        await self._add_to_book(order)
        
        # Record user's order
        self.user_orders[user_id].append(order_id)
        
        return order

    async def _validate_order(self, order: Order) -> bool:
        """Validate order parameters"""
        if order.side not in ('buy', 'sell'):
            return False
        if order.type not in ('limit', 'market'):
            return False
        if order.amount <= 0:
            return False
        if order.type == 'limit' and order.price <= 0:
            return False
        return True

    async def _add_to_book(self, order: Order):
        """Add order to the appropriate price level"""
        book = self.bids if order.side == 'buy' else self.asks
        
        if order.price not in book:
            book[order.price] = []
        book[order.price].append(order)
        self.orders[order.id] = order
        
        await self.match_orders()

    async def match_orders(self):
        """Match orders using price-time priority"""
        while self._can_match():
            best_bid_price, best_bid_orders = self.bids.peekitem(0)
            best_ask_price, best_ask_orders = self.asks.peekitem(0)
            
            bid_order = best_bid_orders[0]
            ask_order = best_ask_orders[0]
            
            trade_amount = min(
                bid_order.amount - bid_order.filled,
                ask_order.amount - ask_order.filled
            )
            
            await self.execute_trade(bid_order, ask_order, trade_amount, best_bid_price)
            await self._cleanup_orders(bid_order, ask_order)

    def _can_match(self) -> bool:
        """Check if matching is possible"""
        return (
            bool(self.bids) and 
            bool(self.asks) and 
            self.bids.peekitem(0)[0] >= self.asks.peekitem(0)[0]
        )

    async def _cleanup_orders(self, bid_order: Order, ask_order: Order):
        """Remove or update filled orders"""
        for order, book in [(bid_order, self.bids), (ask_order, self.asks)]:
            if order.filled >= order.amount:
                price_level = book[order.price]
                price_level.remove(order)
                if not price_level:
                    book.pop(order.price)
                order.status = 'filled'

    async def execute_trade(self, bid_order: Order, ask_order: Order, amount: float, price: float):
        """Execute trade between two orders"""
        bid_order.filled += amount
        ask_order.filled += amount
        
        # In a real implementation, these would be database operations
        await self._update_balances(bid_order.user_id, ask_order.user_id, amount, price)
        await self._broadcast_trade(amount, price)

    async def _update_balances(self, buyer_id: int, seller_id: int, amount: float, price: float):
        """Update user balances after trade"""
        # Implement actual balance updates here
        pass

    async def _broadcast_trade(self, amount: float, price: float):
        """Notify systems about the trade"""
        # Implement market data feed here
        pass

    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an existing order"""
        if order_id not in self.orders:
            return False
            
        order = self.orders[order_id]
        book = self.bids if order.side == 'buy' else self.asks
        
        if order.price in book:
            book[order.price].remove(order)
            if not book[order.price]:
                book.pop(order.price)
        
        order.status = 'canceled'
        return True

    def get_order(self, order_id: str) -> Optional[Order]:
        """Retrieve order by ID"""
        return self.orders.get(order_id)

    def get_user_orders(self, user_id: int) -> list[Order]:
        """Get all orders for a user"""
        return [self.orders[oid] for oid in self.user_orders.get(user_id, [])]
    
    async def get_market_depth(self, depth: int = 10) -> dict:
        """Get order book depth"""
        return {
            "bids": [{"price": p, "amount": sum(o.amount for o in orders)} 
                    for p, orders in list(self.bids.items())[:depth]],
            "asks": [{"price": p, "amount": sum(o.amount for o in orders)} 
                    for p, orders in list(self.asks.items())[:depth]]
        }
    
    async def validate_order_balance(self, user_id: int, order: Order) -> bool:
        """Check user has sufficient balance"""
        # Implement actual balance check from database
        return True
    
    async def persist_order(self, session: AsyncSession, order: Order) -> None:
        """Save order to database"""
        # Implement database persistence
        pass