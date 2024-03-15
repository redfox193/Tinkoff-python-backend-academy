from typing import Any
from fastapi import HTTPException, status
from pydantic import BaseModel


class KeyValue(BaseModel):  # Used to validate JSON request body in /set
    key: str | Any = None
    value: str | Any = None


class DivisionRequest(BaseModel):  # Used to validate JSON request body in /devide
    dividend: float | int | Any = None
    divider: float | int | Any = None


def check_fields(data: BaseModel, types: list[type]):
    for field_name, field_value in vars(data).items():
        if field_value is None or type(field_value) not in types:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)


def validate_KeyValue(data: KeyValue):  # Validate existence of right keys and their types
    check_fields(data, [str])
    return data


def validate_DivisionRequest(data: DivisionRequest):  # Validate existence of right keys and their types
    check_fields(data, [float, int])
    return data