import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "VoxNR API")
    APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
    DATABASE_URL = os.getenv("DATABASE_URL")


settings = Settings()