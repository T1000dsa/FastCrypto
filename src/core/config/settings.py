from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path 
from fastapi.templating import Jinja2Templates

from src.core.config.models import (
    RunConfig, 
    Current_ApiPrefix,
    Mode, 
    DatabaseConfig, 
    RedisSettings, 
    JwtConfig, 
    BinanceService,
    CorsSettings,
    field_validator
    )


base_dir = Path(__file__).parent.parent.parent
frontend_root = base_dir / 'frontend' / 'templates'
templates = Jinja2Templates(directory=frontend_root)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        env_prefix='FAST__',
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    # Runtime config
    run: RunConfig
    prefix: Current_ApiPrefix = Current_ApiPrefix()
    mode: Mode
    cors:CorsSettings

    # Services
    db: DatabaseConfig
    redis: RedisSettings
    jwt:JwtConfig

    # Api Clients
    Bin:BinanceService

    #elastic:ElasticSearch = ElasticSearch()
    #email:Email_Settings = Email_Settings()

    @field_validator('jwt')
    def validate_jwt_key_length(cls, v):
        if len(v.key.get_secret_value()) < 32:
            raise ValueError("JWT key must be at least 32 characters long")
        return v


    def is_prod(self):
        if self.mode.mode == 'PROD':
            return True
        return False


settings = Settings()
if settings.is_prod():
    raise Exception("Production mode requires additional configuration. Please set up PROD environment properly.")