from fastapi import FastAPI

from src.order_service.kafka.producer import start_producer, stop_producer

app = FastAPI()


@app.on_event('startup')
async def startup():
    await start_producer()


@app.on_event('shutdown')
async def shutdown():
    await stop_producer()
