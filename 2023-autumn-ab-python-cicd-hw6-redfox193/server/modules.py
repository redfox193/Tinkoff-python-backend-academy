from typing import Any
from fastapi import HTTPException, status
from pydantic import BaseModel


class KeyValue(BaseModel):  # Used to validate JSON request body in /set
    key: str | Any = None
    value: str | Any = None


class DivisionRequest(
    BaseModel
):  # Used to validate JSON request body in /devide
    dividend: float | int | Any = None
    divider: float | int | Any = None


def check_fields(data: BaseModel, types: list[type]) -> None:
    for field_value in vars(data).values():
        if field_value is None or type(field_value) not in types:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)


def validate_key_value(
    data: KeyValue,
) -> KeyValue:  # Validate existence of right keys and their types
    check_fields(data, [str])
    return data


def validate_division_request(
    data: DivisionRequest,
) -> DivisionRequest:  # Validate existence of right keys and their types
    check_fields(data, [float, int])
    return data
