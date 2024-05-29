from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI

from .routers import users, events, coupons, recommendations
from .data.dataframe import BettingDataDataframe

# The order matters here. More at https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#sqlmodel-metadata-order-matters
from .dependencies.database import create_db_and_tables

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

logger = logging.getLogger("api")
# logger.disabled = True


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(events.router)
app.include_router(coupons.router)
app.include_router(recommendations.router)

df = BettingDataDataframe("./api/data/dummy.json")


@app.get("/")
def read_root():
    return {"msg": "Hello World"}


if __name__ == "__main__":
    import uvicorn
    from .log_conf import LOGGING_CONFIG

    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8098,
        log_config=LOGGING_CONFIG,
        reload=True,
    )
