from .utils import get_all_events
from random import sample


def random_recommendation():
    num_of_recommendations = 3
    all_events = get_all_events()
    recommendations = sample(all_events, num_of_recommendations)
    return recommendations
