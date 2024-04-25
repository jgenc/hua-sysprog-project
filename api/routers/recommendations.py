import logging

from fastapi import APIRouter

from api.schemas.recommendations import Recommendations
from api.recommendations import most_bet_sport_recommenedation

# from api.dependencies.get_betting_data_df import get_df

router = APIRouter(
    prefix="/recommendation",
    tags=["recommendation"],
)

logger = logging.getLogger("api")


@router.get("/{user_id}", response_model=Recommendations)
def get_recommendation(user_id: int) -> Recommendations:
    recommended_events = most_bet_sport_recommenedation(user_id)
    return Recommendations(events=recommended_events)
