from pydantic import BaseModel


class DayForecast(BaseModel):
    temperature: int
    precipitation: int
