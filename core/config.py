from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "devds98ds902m00a013jk"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()
