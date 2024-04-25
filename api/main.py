import logging

from fastapi import FastAPI

from .routers import users, events, coupons, recommendations
from .data.betting import BettingData

logger = logging.getLogger("api")
# logger.disabled = True

app = FastAPI()
app.include_router(users.router)
app.include_router(events.router)
app.include_router(coupons.router)
app.include_router(recommendations.router)

df = BettingData("./api/data/dummy.json")


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
