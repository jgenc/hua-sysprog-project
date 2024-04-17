from .utils import get_all_events


def random_recommendation():
    num_of_recommendations = 3
    all_events = get_all_events()
    recommendations = [
        event for event in all_events for _ in range(num_of_recommendations)
    ]
    return recommendations
