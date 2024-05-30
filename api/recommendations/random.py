from api.recommendations.utils import get_all_events_df, get_all_events
from random import sample


def random_recommendation() -> list[dict]:
    num_of_recommendations = 3
    all_events = get_all_events()

    if len(all_events) <= num_of_recommendations:
        return all_events

    recommendations = sample(all_events, num_of_recommendations)
    return recommendations
