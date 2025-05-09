from src.core.config.settings import settings


EXCHANGES = {
    "binance": {
        "api_key": settings.BINANCE_API_KEY,
        "secret": settings.BINANCE_SECRET,
        "websocket": True
    }
}

RISK_PARAMETERS = {
    "max_position_size": 0.1,  # 10% of capital
    "daily_loss_limit": 0.05   # 5% daily loss
}