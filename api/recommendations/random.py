from .utils import get_all_events
from random import sample


def random_recommendation() -> list[dict]:
    num_of_recommendations = 3
    all_events = get_all_events()
    recommendations = all_events.sample(num_of_recommendations).to_dict(
        orient="records"
    )
    return recommendations
