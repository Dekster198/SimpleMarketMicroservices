from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    AUTH_HOST: str
    AUTH_PORT: int
    AUTH_USER: str
    AUTH_PASS: str
    AUTH_DB: str

    JWT_SECRET: str

    @property
    def DATABASE_URL_asyncpg(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.AUTH_USER}:{self.AUTH_PASS}"
            f"@{self.AUTH_HOST}:{self.AUTH_PORT}/{self.AUTH_DB}"
        )

    @property
    def DATABASE_URL_psycopg(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.AUTH_USER}:{self.AUTH_PASS}"
            f"@{self.AUTH_HOST}:{self.AUTH_PORT}/{self.AUTH_DB}"
        )

    model_config = SettingsConfigDict(
        env_file="../../.env",
        extra="ignore",
    )


settings = Settings()
