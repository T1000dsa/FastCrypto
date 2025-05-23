from sqlalchemy import select
from datetime import timedelta
import requests

from src.core.services.tasks.celery import celery
from src.core.dependencies.db_helper import db_helper
from src.core.services.database.models.token import TokenModel
from src.core.config.settings import settings

url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

@celery.task
async def async_update_crypto_data(): # data argument
    headers = {"X-CMC_PRO_API_KEY": settings.Con.api}
    params = {"limit": 5000, "convert": "USD"}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()["data"]

    async with db_helper.async_celery_session() as db:
        for token in data:
            db_token = await db.execute(
                select(TokenModel).where(TokenModel.id == token["id"])
            )
            db_token = db_token.scalar_one_or_none()
            
            if not db_token:
                db_token = TokenModel(
                    id=token["id"],
                    name=token["name"],
                    symbol=token["symbol"],
                    price=token["quote"]["USD"]["price"],
                    last_updated=token["last_updated"]
                )
                db.add(db_token)
            else:
                db_token.price = token["quote"]["USD"]["price"]
                db_token.last_updated = token["last_updated"]
    
    return "Updated crypto data!"

# Schedule monthly updates
celery.conf.beat_schedule = {
    'update-crypto-monthly': {
        'task': 'celery_app.update_crypto_data',
        'schedule': timedelta(days=30),  # Runs every 30 days
    },
}