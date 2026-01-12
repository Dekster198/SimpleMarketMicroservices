import json

from aiokafka import AIOKafkaConsumer

from src.product_service.database import async_session_factory
from src.product_service.services.product_reservation_service import ProductReservationService

KAFKA_TOPIC = 'order.events'
KAFKA_BOOTSTRAP_SERVERS = 'kafka:9092'
GROUP_ID = 'product-service'


async def handle_message(message: dict):
    event = message['event']
    order_id = message['order_id']

    async with async_session_factory() as session:
        if event == 'order.created':
            for item in message['items']:
                await ProductReservationService.reserve(
                    session=session,
                    order_id=order_id,
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                )
        elif event == 'order.canceled':
            await ProductReservationService.release(
                session=session,
                order_id=order_id
            )
        elif event == 'order.paid':
            await ProductReservationService.commit(
                session=session,
                order_id=order_id
            )


async def start_consumer():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        enable_auto_commit=True
    )

    await consumer.start()
    try:
        async for msg in consumer:
            await handle_message(msg.value)
    finally:
        await consumer.stop()
