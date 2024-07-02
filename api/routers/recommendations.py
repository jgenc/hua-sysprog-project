import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from api.models.recommendations import Recommendation, RecommendationWithEvents
from api.models.user import User

from api.recommendations.frequency import most_bet_sport_recommenedation
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
    all_user_ids = session.exec(select(User.id)).all()

    for user_id in all_user_ids:
        # This is the part that can be substituted with a different recommendation algorithm
        # The recommendation algorithm should just return a list of events
        results = most_bet_sport_recommenedation(user_id)
        new_recommendation = Recommendation(user_id=user_id, events=results)
        session.add(new_recommendation)
        session.commit()
        session.refresh(new_recommendation)

    return f"Recommendations generated for {len(all_user_ids)} users."