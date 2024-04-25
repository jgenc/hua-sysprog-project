from api.data.dataframe import BettingDataDataframe


async def get_df():
    return BettingDataDataframe("./api/data/dummy.json")
