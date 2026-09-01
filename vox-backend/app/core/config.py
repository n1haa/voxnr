import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "VoxNR API")
    APP_VERSION = os.getenv("APP_VERSION", "0.1.0")

    DATABASE_URL = os.getenv("DATABASE_URL")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
    )

    REFRESH_TOKEN_EXPIRE_DAYS = int(
        os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")
    )

    S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
    S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
    S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
    S3_BUCKET = os.getenv(
        "S3_BUCKET",
        "voxnr-dialogues",
    )
    S3_REGION = os.getenv(
        "S3_REGION",
        "us-east-1",
    )
    S3_ADDRESSING_STYLE = os.getenv(
        "S3_ADDRESSING_STYLE",
        "path",
    )

    S3_PRESIGNED_URL_EXPIRE_SECONDS = int(
        os.getenv(
            "S3_PRESIGNED_URL_EXPIRE_SECONDS",
            "900",
        )
    )

    S3_SERVER_SIDE_ENCRYPTION = os.getenv(
        "S3_SERVER_SIDE_ENCRYPTION",
    )

    CELERY_BROKER_URL = os.getenv(
        "CELERY_BROKER_URL",
        "redis://127.0.0.1:6379/0",
    )


settings = Settings()