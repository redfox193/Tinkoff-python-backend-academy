import random
from typing import List

from fastapi import APIRouter

from weather_server.contracts import DayForecast

router = APIRouter()


@router.get("/", response_model=List[DayForecast])
async def get_month_forecast() -> List[DayForecast]:
    """
    Returns a list of day forecasts for the next 30 days.

    Returns:
        List[DayForecast]: A list of `DayForecast` objects representing the forecast for each day.
    """
    forecast = []
    for i in range(30):
        forecast.append(
            DayForecast(
                temperature=random.randint(255, 300),
                precipitation=random.randint(10, 50),
            )
        )
    return forecast
