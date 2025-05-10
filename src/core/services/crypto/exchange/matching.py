from collections import defaultdict
import asyncio


class MatchingEngine:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.bids = defaultdict(list)
            cls._instance.asks = defaultdict(list)
        return cls._instance
    
    async def add_order(self, order):
        # Simplified matching logic
        if order.side == "buy":
            book = self.bids
        else:
            book = self.asks
            
        book[order.price].append(order)
        await self.match_orders()
    
    async def match_orders(self):
        # Basic price-time priority matching
        while self.bids and self.asks:
            best_bid = max(self.bids.keys())
            best_ask = min(self.asks.keys())
            
            if best_bid >= best_ask:
                # Execute trade
                await self.execute_trade(best_bid, best_ask)
            else:
                break