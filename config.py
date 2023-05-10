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
    SEPOLIA_RPC_URL: str = os.getenv('SEPOLIA_RPC_URL')
    PRIVATE_KEY: str = os.getenv('PRIVATE_KEY')
    ACCOUNT_ADDRESS: str = os.getenv('ACCOUNT_ADDRESS')
    EFToken_ContractAddress: str = os.getenv('EFToken_ContractAddress')

    class Config:
        env_file = ".env"


settings = Settings()