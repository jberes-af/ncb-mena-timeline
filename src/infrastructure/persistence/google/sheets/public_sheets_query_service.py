# /src/infrastructure/persistence/google/sheets/public_sheets_query_service.py

import requests


class PublicGoogleSheetsQueryService:
    def __init__(
        self,
        *,
        api_key: str,
    ) -> None:
        self._api_key = api_key

    def read_values(
        self,
        *,
        spreadsheet_id: str,
        range_a1: str,
    ) -> list[dict[str, str]]:
        url = (
            "https://sheets.googleapis.com/v4/spreadsheets/"
            f"{spreadsheet_id}/values/{range_a1}"
        )

        response = requests.get(
            url,
            params={
                "key": self._api_key,
                "majorDimension": "ROWS",
            },
            timeout=20,
        )

        response.raise_for_status()

        values = response.json().get("values", [])

        if not values:
            return []

        headers = [str(value).strip() for value in values[0]]

        rows: list[dict[str, str]] = []

        for raw_row in values[1:]:
            row = {
                headers[index]: (
                    str(raw_row[index]).strip()
                    if index < len(raw_row)
                    else ""
                )
                for index in range(len(headers))
            }

            rows.append(row)

        return rows
