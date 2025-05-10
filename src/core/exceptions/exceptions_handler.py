from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse


router = APIRouter()
class CustomException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code

@router.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "success": False},
    )