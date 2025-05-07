from fastapi import APIRouter


router = APIRouter()

@router.get('/ping')
async def health():
    return 'pong'