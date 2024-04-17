from ..schemas import User, Event, Coupon, Selection, Recommendations
import random
import string
import json
from datetime import datetime, timedelta

countries = [
    "AFG",
    "ALA",
    "ALB",
    "DZA",
    "ASM",
    "AND",
    "AGO",
    "AIA",
    "ATA",
    "ATG",
    "ARG",
    "ARM",
    "ABW",
    "AUS",
    "AUT",
    "AZE",
    "BHS",
    "BHR",
    "BGD",
    "BRB",
    "BLR",
    "BEL",
    "BLZ",
    "BEN",
    "BMU",
    "BTN",
    "BOL",
    "BES",
    "BIH",
    "BWA",
    "BVT",
    "BRA",
    "IOT",
    "BRN",
    "BGR",
    "BFA",
    "BDI",
    "CPV",
    "KHM",
    "CMR",
    "CAN",
    "CYM",
    "CAF",
    "TCD",
    "CHL",
    "CHN",
    "CXR",
    "CCK",
    "COL",
    "COM",
    "COG",
    "COD",
    "COK",
    "CRI",
    "CIV",
    "HRV",
    "CUB",
    "CUW",
    "CYP",
    "CZE",
    "DNK",
    "DJI",
    "DMA",
    "DOM",
    "ECU",
    "EGY",
    "SLV",
    "GNQ",
    "ERI",
    "EST",
    "SWZ",
    "ETH",
    "FLK",
    "FRO",
    "FJI",
    "FIN",
    "FRA",
    "GUF",
    "PYF",
    "ATF",
    "GAB",
    "GMB",
    "GEO",
    "DEU",
    "GHA",
    "GIB",
    "GRC",
    "GRL",
    "GRD",
    "GLP",
    "GUM",
    "GTM",
    "GGY",
    "GIN",
    "GNB",
    "GUY",
    "HTI",
    "HMD",
    "VAT",
    "HND",
    "HKG",
    "HUN",
    "ISL",
    "IND",
    "IDN",
    "IRN",
    "IRQ",
    "IRL",
    "IMN",
    "ISR",
    "ITA",
    "JAM",
    "JPN",
    "JEY",
    "JOR",
    "KAZ",
    "KEN",
    "KIR",
    "PRK",
    "KOR",
    "KWT",
    "KGZ",
    "LAO",
    "LVA",
    "LBN",
    "LSO",
    "LBR",
    "LBY",
    "LIE",
    "LTU",
    "LUX",
    "MAC",
    "MDG",
    "MWI",
    "MYS",
    "MDV",
    "MLI",
    "MLT",
    "MHL",
    "MTQ",
    "MRT",
    "MUS",
    "MYT",
    "MEX",
    "FSM",
    "MDA",
    "MCO",
    "MNG",
    "MNE",
    "MSR",
    "MAR",
    "MOZ",
    "MMR",
    "NAM",
    "NRU",
    "NPL",
    "NLD",
    "NCL",
    "NZL",
    "NIC",
    "NER",
    "NGA",
    "NIU",
    "NFK",
    "MKD",
    "MNP",
    "NOR",
    "OMN",
    "PAK",
    "PLW",
    "PSE",
    "PAN",
    "PNG",
    "PRY",
    "PER",
    "PHL",
    "PCN",
    "POL",
    "PRT",
    "PRI",
    "QAT",
    "REU",
    "ROU",
    "RUS",
    "RWA",
    "BLM",
    "SHN",
    "KNA",
    "LCA",
    "MAF",
    "SPM",
    "VCT",
    "WSM",
    "SMR",
    "STP",
    "SAU",
    "SEN",
    "SRB",
    "SYC",
    "SLE",
    "SGP",
    "SXM",
    "SVK",
    "SVN",
    "SLB",
    "SOM",
    "ZAF",
    "SGS",
    "SSD",
    "ESP",
    "LKA",
    "SDN",
    "SUR",
    "SJM",
    "SWE",
    "CHE",
    "SYR",
    "TWN",
    "TJK",
    "TZA",
    "THA",
    "TLS",
    "TGO",
    "TKL",
    "TON",
    "TTO",
    "TUN",
    "TUR",
    "TKM",
    "TCA",
    "TUV",
    "UGA",
    "UKR",
    "ARE",
    "GBR",
    "USA",
    "UMI",
    "URY",
    "UZB",
    "VUT",
    "VEN",
    "VNM",
    "VGB",
    "VIR",
    "WLF",
    "ESH",
    "YEM",
    "ZMB",
    "ZWE",
]
currencies = ["USD", "EUR", "YEN"]
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
        return (datetime.now() + timedelta(days=random.randint(0, 365))).isoformat()
    return (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat()


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
        birth_year=random.randint(1950, 2003),
        country=random_country(),
        currency=random_currency(),
        gender=random.choice(["Male", "Female"]),
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


def create_selection(event_id: str) -> Selection:
    return Selection(
        event_id=event_id,
        odds=random.uniform(1.0, 3.0),
    )


events = []
for i in range(100):
    events.append(create_event(str(random.randint(1, 100_000))))


def random_event() -> Event:
    return random.choice(events)


def create_coupon(user_id: int, coupon_id: int) -> Coupon:
    return Coupon(
        coupon_id=coupon_id,
        selections=[
            Selection(event_id=random_event().event_id, odds=random.uniform(1.0, 3.0))
            for _ in range(random.randint(1, 5))
        ],
        stake=random.uniform(10.0, 1000.0),
        timestamp=random_date(),
        user_id=user_id,
    )


users = []
for i in range(100):
    users.append(create_user(random.randint(1, 100_000)))


coupons = []
for i in range(100):
    coupons.append(
        create_coupon(random.randint(1, 100_000), random.randint(1, 100_000))
    )

# run in root of project with `python -m api.tools.create_dummy`
# Write data to file
with open("./api/tools/dummy.json", "w") as f:
    json.dump(
        {
            "users": [user.dict() for user in users],
            "events": [event.dict() for event in events],
            # "recommendations": [rec.dict() for rec in recommendations],
            "coupons": [coupon.dict() for coupon in coupons],
        },
        f,
    )
