from fastapi import APIRouter, Depends, HTTPException, status
import requests

from src.core.config.settings import settings
from src.core.dependencies.auth_deps import GET_CURRENT_ACTIVE_USER


router = APIRouter()

@router.get("/get_price/{SYMB}")
async def get_crypto_price(user:GET_CURRENT_ACTIVE_USER, SYMB="BTC"):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    params = {"symbol": SYMB, "convert": "USD"}
    headers = {"X-CMC_PRO_API_KEY": settings.Con.api.get_secret_value()}  # Get from CoinMarketCap
    response = requests.get(url, headers=headers, params=params)
    return response.json()

@router.get('/get_all_tokens')
async def get_all_tokens(user:GET_CURRENT_ACTIVE_USER):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": settings.Con.api.get_secret_value(),
    }
    response = requests.get(url, headers=headers)
    print(response.json())
    return 200