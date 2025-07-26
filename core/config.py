from pydantic import BaseSettings

class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_USER: str = "render"
    DB_PASSWORD: str
    DB_NAME: str = "buildbot"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    ENV: str = "production"
class BitConfig:
    API_KEY = "ваш_api_ключ"
    API_URL = "https://bit.il/api/v1/payment"


settings = Settings()
