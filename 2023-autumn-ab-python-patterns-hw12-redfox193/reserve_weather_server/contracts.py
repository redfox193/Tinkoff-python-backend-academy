from pydantic import BaseModel


class DayForecast(BaseModel):
    data: str
