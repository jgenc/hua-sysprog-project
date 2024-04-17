from ..schemas import Event
from .utils import get_user_events, get_all_events
from .random import random_recommendation
from pprint import pprint
import random


def most_bet_sport_recommenedation(user_id: int) -> list[Event]:
    user_events = get_user_events(user_id)

    # No user events, return random
    if len(user_events) == 0:
        return random_recommendation()

    all_events = get_all_events()
    user_sports = [event["sport"] for event in user_events]
    sport_frequency = {sport: user_sports.count(sport) for sport in user_sports}

    selected_sport = max(sport_frequency, key=sport_frequency.get)

    # TODO: Make this configurable
    num_of_recommendations = 3

    eligable_events = [
        event
        for event in all_events
        if event["sport"] == selected_sport and event not in user_events
    ]

    recommendations = random.sample(eligable_events, num_of_recommendations)

    # TODO: Add debug mode
    print("User Sports Frequency Report")
    print("=" * 80)
    print(f"User ID\t| {user_id}")
    print("-" * 20)
    print("Sport\t| Frequency")
    print("-" * 20)
    print(
        "\n".join(
            [f"{sport}\t| {frequency}" for sport, frequency in sport_frequency.items()]
        )
    )
    print("-" * 20)
    print("Recommendations")
    print("-" * 20)
    pprint(recommendations)

    return [Event(**recommendation) for recommendation in recommendations]
