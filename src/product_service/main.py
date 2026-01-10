from fastapi import FastAPI

from src.product_service.routers.product_router import router

app = FastAPI()


app.include_router(router)

