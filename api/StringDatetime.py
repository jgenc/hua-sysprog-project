from datetime import datetime
from typing import Annotated

from pydantic.functional_validators import AfterValidator


def check_timestamp(timestamp: str) -> str:
    assert datetime.fromisoformat(timestamp), "Invalid timestamp"
    return str(timestamp)


StringDatetime = Annotated[str, AfterValidator(check_timestamp)]
