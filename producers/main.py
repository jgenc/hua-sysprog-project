# from enum import Enum
import json
import asyncio
from os import environ

from fastapi import FastAPI
from aiokafka import AIOKafkaProducer

from producers.models.user import UserCreate
from producers.models.event import EventCreate
from producers.models.coupon import CouponCreate

app = FastAPI()

bootstrap_server = environ.get("BOOTSTRAP_SERVER", "localhost:9094")
print(f"[\x1b[1;31mDEBUG\x1b[0m] Bootstrapping to {bootstrap_server}")

# TODO Create some enum for topics


async def produce(topic: str, encoded_data: dict):
    try:
        producer = AIOKafkaProducer(bootstrap_servers=bootstrap_server)
        await producer.start()
        print("[\x1b[1;31mDEBUG\x1b[0m] Producer started.")
        await producer.send_and_wait(topic, encoded_data)
        # print(f"[\x1b[1;31mDEBUG\x1b[0m] Produced to {topic} with data {data}")
    except Exception as e:
        print(f"[\x1b[1;31mDEBUG\x1b[0m] Error: {e}")
    finally:
        print("[\x1b[1;31mDEBUG\x1b[0m] Producer stopped.")
        await producer.stop()


@app.post("/users")
def post_user_kafka(user: UserCreate):
    encoded_user = user.model_dump_json()
    data = {"op": "users", "data": encoded_user}
    data = json.dumps(data).encode()
    try:
        x = asyncio.run(produce("users", data))
        return "OK, PRODUCED"
    except Exception as e:
        print(e)
        return "ERROR, NOT PRODUCED"


@app.post("/events")
def post_event_kafka(event: EventCreate):
    encoded_event = event.model_dump_json()
    data = {"op": "events", "data": encoded_event}
    data = json.dumps(data).encode()
    try:
        x = asyncio.run(produce("events", data))
        return "OK, PRODUCED"
    except Exception as e:
        print(e)
        return "ERROR, NOT PRODUCED"


@app.post("/coupons")
def post_coupon_kafka(coupon: CouponCreate):
    encoded_coupon = coupon.model_dump_json()
    data = {"op": "coupons", "data": encoded_coupon}
    data = json.dumps(data).encode()
    try:
        x = asyncio.run(produce("coupons", data))
        return "OK, PRODUCED"
    except Exception as e:
        print(e)
        return "ERROR, NOT PRODUCED"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "producers.main:app",
        host="0.0.0.0",
        port=8099,
        reload=True,
    )
