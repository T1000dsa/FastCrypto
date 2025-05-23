from fastapi import Depends, Request
from jose import JWTError, jwt
from typing import Annotated, Optional

from src.core.services.auth.token_service import TokenService
from src.core.services.auth.user_service import UserService
from src.core.dependencies.db_helper import DBDI
from src.core.services.database.models.user import UserModel
from src.core.config.settings import settings
from src.core.config.auth_config import (
    credentials_exception, 
    inactive_user_exception,
    ACCESS_TYPE
)

def get_token_from_cookie(request: Request) -> Optional[str]:
    return request.cookies.get(ACCESS_TYPE)

async def get_token_service() -> TokenService:
    return TokenService(
        secret_key=settings.jwt.key,
        algorithm=settings.jwt.algorithm
    )

async def get_auth_service(
    session: DBDI,
    token_service: TokenService = Depends(get_token_service)
) -> UserService:
    return UserService(
        session=session,
        token_service=token_service
    )

async def get_current_user(
    token: str = Depends(get_token_from_cookie),
    auth_service: UserService = Depends(get_auth_service)
) -> UserModel:
    if token is None:
        raise credentials_exception
    
    if token is None:
        raise credentials_exception
    
    try:
        payload = await auth_service.token_service.verify_token(token, ACCESS_TYPE)
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception
            
    except JWTError as e:
        raise credentials_exception
    
    user = await auth_service.get_user_by_id(int(user_id))
    if user is None:
        raise credentials_exception
        
    return user

async def get_current_active_user(
    current_user: UserModel = Depends(get_current_user)
) -> UserModel:
    if not current_user.is_active:
        raise inactive_user_exception
    return current_user


GET_TOKEN_SERVICE = Annotated[TokenService, Depends(get_token_service)]
GET_AUTH_SERVICE = Annotated[UserService, Depends(get_auth_service)]
GET_CURRENT_USER = Annotated[UserModel, Depends(get_current_user)]
GET_CURRENT_ACTIVE_USER = Annotated[UserModel, Depends(get_current_active_user)]