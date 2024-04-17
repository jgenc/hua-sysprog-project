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

    # NOTE
    # What happens if there are multiple sports with the same frequency?
    sport_frequency = user_events["sport"].value_counts()
    selected_sport = user_events["sport"].value_counts().idxmax()

    # TODO: Make this configurable
    num_of_recommendations = 3

    all_events = get_all_events()

    eligable_events = all_events[all_events["sport"] == selected_sport]
    recommendations = eligable_events.sample(num_of_recommendations).to_dict(
        orient="records"
    )

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
