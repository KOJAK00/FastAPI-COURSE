from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

    DB_CONNECTION : str
    SECRET_KEY : str
    ALGORITHIM : str
    EXP_TIME : int

settings = Settings()

