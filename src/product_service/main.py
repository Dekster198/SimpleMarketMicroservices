import asyncio

from fastapi import FastAPI

from routers.product_router import router
from src.product_service.consumers.order_consumer import start_consumer

app = FastAPI()


app.include_router(router)


@app.on_event('startup')
async def startup():
    asyncio.create_task(start_consumer())
