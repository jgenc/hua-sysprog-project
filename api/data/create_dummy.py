import random
import string
import json
from datetime import datetime, timedelta

from api.models.event import EventCreate as Event
from api.models.coupon import CouponWithSelections as Coupon
from api.models.user import User

countries = ["US", "UK", "DE", "FR", "GR", "AL", "IT", "ES", "JPN"]
currencies = ["USD", "EUR", "JPY", "GBP"]
sports = ["Football", "Basketball", "Volley", "Tennis", "Golf", "Rugby", "Hockey"]
leagues = {
    "Football": ["Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1"],
    "Basketball": ["NBA", "Euroleague", "ACB", "VTB"],
    "Volley": ["World League", "Champions League", "Superliga", "A1"],
    "Tennis": ["ATP", "WTA"],
    "Golf": ["PGA", "European Tour"],
    "Rugby": ["Six Nations", "Super Rugby"],
    "Hockey": ["NHL", "KHL"],
}
participants = {
    "Football": ["Real Madrid", "Barcelona", "Manchester United", "Liverpool"],
    "Basketball": ["Los Angeles Lakers", "Golden State Warriors", "Real Madrid"],
    "Volley": ["Zenit Kazan", "Lube Civitanova", "Trentino Volley"],
    "Tennis": ["Rafael Nadal", "Novak Djokovic", "Roger Federer"],
    "Golf": ["Tiger Woods", "Rory McIlroy", "Jordan Spieth"],
    "Rugby": ["New Zealand", "England", "South Africa"],
    "Hockey": ["Montreal Canadiens", "Toronto Maple Leafs", "New York Rangers"],
}


def random_country() -> str:
    return random.choice(countries)


def random_currency() -> str:
    return random.choice(currencies)


def random_sport() -> str:
    return random.choice(sports)


def random_string(length: int) -> str:
    return "".join(random.choices(string.ascii_letters, k=length))


def random_date(after_than_today: bool = False) -> str:
    if after_than_today:
        x = datetime.now() + timedelta(days=random.randint(0, 365))
    else:
        x = datetime.now() - timedelta(days=random.randint(0, 365))
    return str(x)


def random_league(sport: str) -> str:
    return random.choice(leagues[sport])


def random_participant(sport: str) -> str:
    sport_1 = random.choice(participants[sport])
    participants_copy = participants[sport].copy()
    participants_copy.remove(sport_1)
    sport_2 = random.choice(participants_copy)
    return [sport_1, sport_2]


def create_user(user_id: int) -> User:
    return User(
        birth_year=random.randint(1950, 2002),
        country=random_country(),
        currency=random_currency(),
        gender=random.choice(["M", "F"]),
        registration_date=random_date(),
        user_id=user_id,
    )


def create_event(event_id: str) -> Event:
    chosen_sport = random_sport()
    return Event(
        begin_timestamp=random_date(),
        end_timestamp=random_date(after_than_today=True),
        country=random_country(),
        event_id=event_id,
        sport=chosen_sport,
        league=random_league(chosen_sport),
        participants=random_participant(chosen_sport),
    )


events = []
for i in range(100):
    events.append(create_event(i))


def random_event() -> Event:
    return random.choice(events)


def create_coupon(user_id: int, coupon_id: int) -> Coupon:
    return Coupon(
        id=coupon_id,
        selections=[
            {"event_id": random.randint(1, 100), "odds": random.uniform(1.0, 3.0)}
            for _ in range(random.randint(1, 5))
        ],
        stake=random.uniform(10.0, 1000.0),
        timestamp=random_date(),
        user_id=user_id,
    )


users = []
for i in range(100):
    users.append(create_user(i))


coupons = []
for i in range(100):
    coupons.append(create_coupon(random.randint(1, 100), i))

# Appending a user with id 0 to the list of users for testing
users.append(
    User(
        birth_year=1990,
        country="US",
        currency="USD",
        gender="M",
        registration_date="2021-01-01T00:00:00",
        user_id=0,
    )
)

# run in root of project with `python -m api.tools.create_dummy`
# Write data to file
with open("./api/data/dummy.json", "w") as f:
    json.dump(
        {
            "users": [user.model_dump() for user in users],
            "events": [event.model_dump() for event in events],
            # "recommendations": [rec.dict() for rec in recommendations],
            "coupons": [coupon.model_dump() for coupon in coupons],
        },
        f,
    )
