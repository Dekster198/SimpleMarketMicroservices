import orjson
from aiokafka import AIOKafkaProducer

KAFKA_BOOTSTRAP_SERVERS = 'kafka:9092'


producer: AIOKafkaProducer | None = None


async def start_producer():
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: orjson.dumps(v)
    )
    await producer.start()


async def stop_producer():
    global producer
    if producer:
        await producer.stop()


async def send_event(topic: str, value: dict):
    if not producer:
        raise RuntimeError('Kafka producer not started')

    await producer.send_and_wait(topic, value)
