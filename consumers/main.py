from os import environ
import asyncio
from aiokafka import AIOKafkaConsumer
import httpx
import json
import os

bootstrap_server = environ.get("BOOTSTRAP_SERVER", "kafka:9092")
TOPICS = os.environ.get("TOPIC")

async def consumer(topics: str):
    try:
        consumer = AIOKafkaConsumer(
            topics,
            bootstrap_servers=bootstrap_server,
        )
        await consumer.start()
        print(
            f"[\x1b[1;31mDEBUG\x1b[0m] Consumer started on topic {topics}.", flush=True
        )

        async for msg in consumer:
            # x = f"[\x1b[1;31mDEBUG\x1b[0m] Consumed: {msg.topic}, {msg.partition}, {msg.offset}, {msg.key}, {msg.value}, {msg.timestamp}"
            # print(x, flush=True)
            json_data = json.loads(msg.value)
            op = json_data.get("op")
            data = json.loads(json_data.get("data"))
            httpx.post(f"http://api:8098/{op}", json=data)
    except Exception as e:
        print(f"[\x1b[1;31mDEBUG\x1b[0m] Error: {e}", flush=True)
    finally:
        # print("[\x1b[1;31mDEBUG\x1b[0m] Consumer stopped.")
        await consumer.stop()
        # loop.stop()


if __name__ == "__main__":
    assert TOPICS != "", "TOPICS environment variable is required for the Consumer to work"

    # print("[\x1b[1;31mDEBUG\x1b[0m] Consumer started.", flush=True)
    asyncio.run(consumer(topics=TOPICS))
