from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()

class ErrorResponse(BaseModel):
    success: bool = False
    error_code: str
    message: str
    details: dict | None = None

class AppException(Exception):
    def __init__(self, error_code: str, message: str, status_code: int, details: dict = None):
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        self.details = details or {}

def create_exception_handler(*exception_classes):
    async def handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error_code=exc.error_code,
                message=exc.message,
                details=exc.details
            ).dict()
        )
    return handler

# Register the handler for multiple exception types
app.add_exception_handler(
    AppException, 
    create_exception_handler(AppException)
)

# Example usage
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    if user_id == "admin":
        raise AppException(
            error_code="ACCESS_DENIED",
            message="Admin access is restricted",
            status_code=403,
            details={"reason": "privileged_account"}
        )
    return {"user_id": user_id}