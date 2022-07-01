from pydantic import BaseSettings


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30
    SECRET_KEY: str = 'O6Pm30ZfK5i-Z8fE7Q78Tw'
    API_URL_PREFIX: str = '/api/v1'


settings = Settings()
