import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from api.data.dataframe import BettingDataDataframe
from api.models.event import (
    Event,
    EventBase,
    Participants,
    EventCreate,
    ParticipantsBase,
)

# from api.dependencies.get_betting_data_df import get_df
from api.dependencies.database import get_session

from api.routers.recommendations import generate_recommendations


router = APIRouter(
    prefix="/events", tags=["events"], dependencies=[Depends(get_session)]
)

logger = logging.getLogger("api")


# @router.get("/random", response_model=Event)
# def get_event_random(df: BettingDataDataframe = Depends(get_df)) -> Event:
#     return Event(**df._events.sample(1).to_dict(orient="records")[0])


@router.get("/{event_id}", response_model=Event)
def read_event(event_id: str, session: Session = Depends(get_session)) -> Event:
    results = session.get(Event, event_id)
    if not results:
        raise HTTPException(status_code=404, detail="Event not found")
    return results


@router.post("", response_model=Event)
def create_event(
    new_event: EventCreate, gen_recommendations: bool = True, session: Session = Depends(get_session)
) -> Event:
    new_participants = ParticipantsBase(
        a=new_event.participants[0], b=new_event.participants[1]
    )

    existing_participants = session.exec(
        select(Participants)
        .where(Participants.a == new_participants.a)
        .where(Participants.b == new_participants.b)
    ).all()
    if len(existing_participants) >= 1:
        participants_id = existing_participants[0].id
    else:
        new_participants = Participants(**new_participants.model_dump())
        session.add(new_participants)
        session.commit()
        session.refresh(new_participants)
        participants_id = new_participants.id

    new_event = Event(
        begin_timestamp=new_event.begin_timestamp,
        end_timestamp=new_event.end_timestamp,
        country=new_event.country,
        league=new_event.league,
        sport=new_event.sport,
        participants_id=participants_id,
    )

    session.add(new_event)
    session.commit()
    session.refresh(new_event)

    # Generate new recommendations
    if gen_recommendations:
        generate_recommendations(session=session)

    return new_event
