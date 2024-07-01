import asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi import APIRouter

loop = asyncio.get_event_loop()
router = APIRouter(prefix="/kafka", tags=["kafka"])


async def produce_to_hello():
    producer = AIOKafkaProducer(bootstrap_servers="localhost:9092", loop=loop)
    await producer.start()
    try:
        await producer.send_and_wait("hello", b"Hello from a FastAPI instance")
    finally:
        await producer.stop()


async def consume_from_hello():
    consumer = AIOKafkaConsumer(
        "hello", bootstrap_servers="localhost:9092", group_id="my-group", loop=loop
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(
                f"Consumed: {msg.topic}, {msg.partition}, {msg.offset}, {msg.key}, {msg.value}, {msg.timestamp}"
            )
    finally:
        await consumer.stop()


@router.get("/kafka/produce")
async def kafka_produce():
    try:
        asyncio.run(await produce_to_hello())
        return "OK, PRODUCED"
    except:
        return "ERROR, NOT PRODUCED"


@router.get("/kafka/consume")
async def kafka_consume():
    try:
        asyncio.run(await consume_from_hello())
        return "OK, CONSUMED"
    except:
        return "ERROR, NOT CONSUMED"
