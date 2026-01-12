from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ORDER_HOST: str
    ORDER_PORT: int
    ORDER_USER: str
    ORDER_PASS: str
    ORDER_DB: str

    @property
    def DATABASE_URL_asyncpg(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.ORDER_USER}:{self.ORDER_PASS}"
            f"@{self.ORDER_HOST}:{self.ORDER_PORT}/{self.ORDER_DB}"
        )

    @property
    def DATABASE_URL_psycopg(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.ORDER_USER}:{self.ORDER_PASS}"
            f"@{self.ORDER_HOST}:{self.ORDER_PORT}/{self.ORDER_DB}"
        )

    model_config = SettingsConfigDict(
        env_file="../../.env",
        extra="ignore",
    )


settings = Settings()
