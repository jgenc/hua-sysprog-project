from api.data.betting import BettingData


async def get_df():
    return BettingData("./api/data/dummy.json")
