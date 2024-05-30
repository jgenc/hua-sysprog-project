from .utils import (
    get_user_events_df,
    get_all_events_df,
    get_user_events,
    get_all_events,
)
from .random import random_recommendation
from pprint import pprint
from random import sample


def most_bet_sport_recommenedation(user_id: int):
    user_events = get_user_events(user_id)

    # No user events, return random
    if len(user_events) == 0:
        return random_recommendation()

    # NOTE
    # What happens if there are multiple sports with the same frequency?
    sport_frequency = {}
    for event in user_events:
        if event.sport not in sport_frequency.keys():
            sport_frequency[event.sport] = 1
        else:
            sport_frequency[event.sport] += 1

    selected_sport = max(sport_frequency, key=sport_frequency.get)

    # sport_frequency = user_events["sport"].value_counts()
    # selected_sport = user_events["sport"].value_counts().idxmax()

    # TODO: Make this configurable
    num_of_recommendations = 3
    all_events = get_all_events()
    eligable_events = [event for event in all_events if event.sport == selected_sport]

    # recommendations = eligable_events.sample(num_of_recommendations).to_dict(
    #     orient="records"
    # )

    if len(eligable_events) <= num_of_recommendations:
        return eligable_events

    recommendations = sample(eligable_events, num_of_recommendations)

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

    return recommendations


if __name__ == "__main__":
    most_bet_sport_recommenedation(20)
