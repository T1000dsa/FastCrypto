from fastapi import APIRouter, Depends, HTTPException, status
import requests

from src.core.config.settings import BLOCKCHAIN_API_URL

router = APIRouter()

@router.get("/balance/{wallet_address}")
async def get_balance(wallet_address: str):
    response = requests.get(f"{BLOCKCHAIN_API_URL}/balance?active={wallet_address}")
    return response.json()
