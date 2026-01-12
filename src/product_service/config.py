from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PRODUCT_HOST: str
    PRODUCT_PORT: int
    PRODUCT_USER: str
    PRODUCT_PASS: str
    PRODUCT_DB: str

    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_ORDER_TOPIC: str = "order.created"
    KAFKA_GROUP_ID: str = "product-service"

    @property
    def DATABASE_URL_asyncpg(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.PRODUCT_USER}:{self.PRODUCT_PASS}"
            f"@{self.PRODUCT_HOST}:{self.PRODUCT_PORT}/{self.PRODUCT_DB}"
        )

    @property
    def DATABASE_URL_psycopg(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.PRODUCT_USER}:{self.PRODUCT_PASS}"
            f"@{self.PRODUCT_HOST}:{self.PRODUCT_PORT}/{self.PRODUCT_DB}"
        )

    model_config = SettingsConfigDict(
        env_file="../../.env",
        extra="ignore",
    )


settings = Settings()
