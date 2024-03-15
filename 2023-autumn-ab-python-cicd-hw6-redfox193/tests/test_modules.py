from fastapi import HTTPException
import pytest
from server.modules import check_fields, KeyValue, DivisionRequest


@pytest.mark.parametrize(
    ("model", "types", "is_valid"),
    [
        (KeyValue(key="test", value="123"), [str], True),
        (KeyValue(key="test", value=None), [str], False),
        (KeyValue(key=123, value="123"), [str], False),
        (DivisionRequest(dividend=10.0, divider=2), [float, int], True),
        (DivisionRequest(dividend=None, divider=2), [float, int], False),
        (
            DivisionRequest(dividend=10.0, divider="string"),
            [float, int],
            False,
        ),
    ],
)
def test_validate_model(
    model: DivisionRequest | KeyValue, types: list[type], is_valid: bool
) -> None:
    try:
        check_fields(model, types)
        assert is_valid is True
    except HTTPException:
        assert is_valid is False
