import logging
import math
from abc import ABC, abstractmethod
from typing import Any

import httpx
from fastapi import APIRouter, HTTPException, status

from config.settings import app_settings
from server import contracts

router = APIRouter()


class WeatherServer(ABC):
    def __init__(self, url: str) -> None:
        self.url = url

    @abstractmethod
    def get(self) -> list[Any]:
        ...

    @abstractmethod
    def forecast_three_days(self) -> contracts.ForecastThreeDays:
        ...

    @abstractmethod
    def forecast_week_average(self) -> contracts.ForecastWeekAv:
        ...

    @abstractmethod
    def forecast_week_pp(self) -> contracts.ForecastWeekPP:
        ...


class MainServer(WeatherServer):
    def get(self) -> list[Any]:
        with httpx.Client() as client:
            response = client.get(f"{self.url}/")
            response.raise_for_status()
            weather_data = list(response.json())
        return weather_data

    def forecast_three_days(self) -> contracts.ForecastThreeDays:
        weather_data = self.get()
        return contracts.ForecastThreeDays(
            forecast_three_days=[
                weather_data[0]['temperature'] / 10,
                weather_data[1]['temperature'] / 10,
                weather_data[2]['temperature'] / 10,
            ]
        )

    def forecast_week_average(self) -> contracts.ForecastWeekAv:
        weather_data = self.get()
        week_average = 0.0
        for i in range(7):
            week_average += weather_data[i]['temperature']
        week_average = math.floor(week_average / 7) / 10
        return contracts.ForecastWeekAv(forecast_week_average=week_average)

    def forecast_week_pp(self) -> contracts.ForecastWeekPP:
        weather_data = self.get()
        week_average = 0.0
        for i in range(7):
            week_average += weather_data[i]['precipitation']
        week_average = math.floor(week_average / 7) / 100
        return contracts.ForecastWeekPP(forecast_week_pp=week_average)


class ReserveServer(WeatherServer):
    def get(self) -> list[Any]:
        with httpx.Client() as client:
            response = client.get(f"{self.url}/month")
            response.raise_for_status()
            weather_data = list(response.json())
            parsed_weather_data = []
            for data in weather_data:
                parsed_weather_data.append(
                    list(map(float, data["data"].split("C:")))
                )
        return parsed_weather_data

    def forecast_three_days(self) -> contracts.ForecastThreeDays:
        weather_data = self.get()
        return contracts.ForecastThreeDays(
            forecast_three_days=[
                weather_data[0][0],
                weather_data[1][0],
                weather_data[2][0],
            ]
        )

    def forecast_week_average(self) -> contracts.ForecastWeekAv:
        weather_data = self.get()
        week_average = 0.0
        for i in range(7):
            week_average += weather_data[i][0]
        week_average = math.floor(week_average / 7 * 10) / 10
        return contracts.ForecastWeekAv(forecast_week_average=week_average)

    def forecast_week_pp(self) -> contracts.ForecastWeekPP:
        weather_data = self.get()
        week_average = 0.0
        for i in range(7):
            week_average += weather_data[i][1]
        week_average = math.floor(week_average / 7 * 100) / 100
        return contracts.ForecastWeekPP(forecast_week_pp=week_average)


class ForecastStrategy(ABC):
    @abstractmethod
    def forecast(
        self, weather_server: WeatherServer  # pylint: disable=unused-argument
    ) -> (
        contracts.ForecastThreeDays
        | contracts.ForecastWeekAv
        | contracts.ForecastWeekPP
    ):
        ...


class Day3Forecast(ForecastStrategy):
    def forecast(
        self, weather_server: WeatherServer
    ) -> contracts.ForecastThreeDays:
        return weather_server.forecast_three_days()


class WeekAverageForecast(ForecastStrategy):
    def forecast(
        self, weather_server: WeatherServer
    ) -> contracts.ForecastWeekAv:
        return weather_server.forecast_week_average()


class WeekPPForecast(ForecastStrategy):
    def forecast(
        self, weather_server: WeatherServer
    ) -> contracts.ForecastWeekPP:
        return weather_server.forecast_week_pp()


class Servers:
    def __init__(self) -> None:
        self.servers: list[WeatherServer] = []

    def add_next(self, weather_server: WeatherServer) -> None:
        self.servers.append(weather_server)

    def forecast(
        self, forecast: ForecastStrategy
    ) -> (
        contracts.ForecastThreeDays
        | contracts.ForecastWeekAv
        | contracts.ForecastWeekPP
        | None
    ):
        for server in self.servers:
            try:
                return forecast.forecast(server)
            except Exception as exp:  # pylint: disable=broad-exception-caught
                logger = logging.getLogger()
                logger.info(
                    "forecast with url: %s failed with exception: %s",
                    server.url,
                    exp,
                )
                continue
        return None


main_server = MainServer(app_settings.weather_server_url)
reserve_server = ReserveServer(app_settings.reserve_weather_server_url)
servers = Servers()
servers.add_next(main_server)
servers.add_next(reserve_server)


@router.get(
    "/forecast_three_days_temp", response_model=contracts.ForecastThreeDays
)
async def weather_report_3d() -> contracts.ForecastThreeDays:
    forecast_data = servers.forecast(Day3Forecast())
    if forecast_data is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str("can't get temperature forecast on three days"),
        )
    return forecast_data  # type: ignore


@router.get(
    "/forecast_week_average_temp", response_model=contracts.ForecastWeekAv
)
async def weather_report_week_av() -> contracts.ForecastWeekAv:
    forecast_data = servers.forecast(WeekAverageForecast())
    if forecast_data is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str("can't get temperature forecast on a week"),
        )
    return forecast_data  # type: ignore


@router.get(
    "/forecast_week_probability_of_precipitation",
    response_model=contracts.ForecastWeekPP,
)
async def weather_report_week_pp() -> contracts.ForecastWeekPP:
    forecast_data = servers.forecast(WeekPPForecast())
    if forecast_data is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str("can't get probability of precipitation on a week"),
        )
    return forecast_data  # type: ignore
