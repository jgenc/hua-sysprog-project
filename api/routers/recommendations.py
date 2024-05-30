import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from api.models.recommendations import Recommendation, RecommendationWithEvents
from api.models.user import User

from api.recommendations import most_bet_sport_recommenedation
from api.dependencies.database import get_session, Session

router = APIRouter(
    prefix="/recommendation",
    tags=["recommendation"],
    dependencies=[Depends(get_session)],
)

logger = logging.getLogger("api")


def get_populated_recommendations(recommendations):
    results_populated = []
    for res in recommendations:
        results_populated.append(
            RecommendationWithEvents(
                id=res.id,
                user_id=res.user_id,
                events=[event.model_dump() for event in res.events],
            )
        )
    return results_populated


@router.get("/{user_id}")
def get_recommendation(
    user_id: int, session: Session = Depends(get_session)
) -> list[RecommendationWithEvents]:
    user_results = session.exec(select(User).where(User.id == user_id)).all()
    if not user_results:
        raise HTTPException(status_code=404, detail="User not found")

    results = session.exec(
        select(Recommendation).where(Recommendation.user_id == user_id)
    ).all()

    return get_populated_recommendations(results)


@router.post("/generate")
def generate_recommendations(session: Session = Depends(get_session)) -> str:
    pass
