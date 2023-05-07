from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    database_hostname: str = os.getenv('DATABASE_HOSTNAME', default='localhost')
    database_port: str = os.getenv('DATABASE_PORT')
    database_password: str = os.getenv('DATABASE_PASSWORD')
    database_name: str = os.getenv('DATABASE_NAME', default='graduate_fastapi')
    database_username: str = os.getenv('DATABASE_USERNAME')
    
    class Config:
        env_file = ".env"


settings = Settings()