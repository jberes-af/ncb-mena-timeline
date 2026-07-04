# /src/infrastructure/services/raw_sheet_parser.py

from dataclasses import MISSING, fields, is_dataclass
from typing import Any, Type, TypeVar, cast

T = TypeVar("T")


def parse_rows_to_raw_models(
        *,
        rows: list[dict[str, str]],
        model_cls: Type[T],
) -> list[T]:
    """
    Convert Google Sheets row dictionaries into raw dataclass models.

    Assumption:
    - Google Sheet column headers match the raw dataclass field names.
    - Raw models mostly keep values as strings.
    - Optional/default dataclass fields may be omitted or blank.
    """

    if not is_dataclass(model_cls):
        raise TypeError(f"{model_cls.__name__} must be a dataclass.")

    return [
        _parse_row_to_raw_model(row=row, model_cls=model_cls)
        for row in rows
    ]


def _parse_row_to_raw_model(
        *,
        row: dict[str, str],
        model_cls: Type[T],
) -> T:
    kwargs: dict[str, Any] = {}

    for field in fields(model_cls):
        raw_value: str | None = row.get(field.name)

        if raw_value is None or str(raw_value).strip() == "":
            if field.default is not MISSING:
                kwargs[field.name] = field.default
                continue

            if field.default_factory is not MISSING:  # type: ignore
                kwargs[field.name] = field.default_factory()  # type: ignore
                continue

            raise KeyError(
                f"Missing required Google Sheet column/value: {field.name} {model_cls}"
            )

        kwargs[field.name] = str(raw_value).strip()

    return cast(T, model_cls(**kwargs))
