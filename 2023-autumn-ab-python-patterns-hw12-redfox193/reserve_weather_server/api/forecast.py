import random
from typing import List

from fastapi import APIRouter

from reserve_weather_server.contracts import DayForecast

router = APIRouter()


@router.get("/month", response_model=List[DayForecast])
async def get_month_forecast() -> List[DayForecast]:
    """
    Retrieves the monthly forecast for the weather.

    Returns:
        A list of DayForecast objects representing the weather forecast for each day of the month.
    """
    forecast = []
    for i in range(30):
        forecast.append(
            DayForecast(
                data=f"{random.randint(250, 300) / 10}C:{random.randint(10, 50) / 100}"
            )
        )
    return forecast
