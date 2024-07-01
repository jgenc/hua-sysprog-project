import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .data.dataframe import BettingDataDataframe

# The order matters here. More at https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#sqlmodel-metadata-order-matters
from .dependencies.database import create_db_and_tables
from .routers import coupons, events, recommendations, users

logger = logging.getLogger("api")
PORT = os.getenv("PORT", 8098)
PORT = int(PORT)


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
        port=PORT,
        log_config=LOGGING_CONFIG,
        reload=True,
    )
