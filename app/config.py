import os
from pydantic_settings import BaseSettings, SettingsConfigDict
DOTENV = os.path.join(os.path.dirname(__file__), ".env")

class Settings(BaseSettings):
    app_name: str
    database_type:str
    database_hostname:str
    database_port:str
    database_password:str
    database_name:str
    database_username:str
    SECRET_KEY:str
    ALGORITHM:str 
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    model_config = SettingsConfigDict(env_file=DOTENV)


settings = Settings()