import logging

from fastapi import APIRouter, Depends, HTTPException
from api.data.dataframe import BettingDataDataframe

from api.schemas.event import Event
from api.dependencies.get_betting_data_df import get_df

router = APIRouter(
    prefix="/event",
    tags=["events"],
)

logger = logging.getLogger("api")


@router.get("/random", response_model=Event)
def get_event_random(df: BettingDataDataframe = Depends(get_df)) -> Event:
    return Event(**df._events.sample(1).to_dict(orient="records")[0])


@router.get("/{event_id}", response_model=Event)
def read_event(event_id: str, df: BettingDataDataframe = Depends(get_df)) -> Event:
    try:
        event = df._events[df._events["event_id"] == event_id].to_dict(
            orient="records"
        )[0]
    except IndexError:
        raise HTTPException(status_code=404, detail="Event not found")

    return Event(**event)


@router.post("", response_model=Event)
def create_event(new_event: Event, df: BettingDataDataframe = Depends(get_df)) -> Event:
    event_exists = False
    if not event_exists:
        raise HTTPException(status_code=501, detail="Not implemented")
