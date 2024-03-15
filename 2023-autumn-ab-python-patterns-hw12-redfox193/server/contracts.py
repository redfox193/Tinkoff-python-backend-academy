from pydantic import BaseModel


class ForecastThreeDays(BaseModel):
    forecast_three_days: list[float]


class ForecastWeekAv(BaseModel):
    forecast_week_average: float


class ForecastWeekPP(BaseModel):
    forecast_week_pp: float


class FoundParents(BaseModel):
    found_parents: list[str]
