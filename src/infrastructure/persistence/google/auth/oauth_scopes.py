# infrastructure/google/auth/oauth_scopes.py

from typing import Literal, Sequence

GoogleAccessMode = Literal["read", "write"]
DriveAccessMode = Literal["none", "read", "write", "all"]

SHEETS_SCOPES_READONLY = ("https://www.googleapis.com/auth/spreadsheets.readonly",)
SHEETS_SCOPES_READWRITE = ("https://www.googleapis.com/auth/spreadsheets",)

DRIVE_SCOPES_READONLY = ("https://www.googleapis.com/auth/drive.readonly",)
DRIVE_SCOPES_FILE_WRITE = ("https://www.googleapis.com/auth/drive.file",)
DRIVE_SCOPES_ALL = ("https://www.googleapis.com/auth/drive",)


def combined_scopes(*, sheets_mode: GoogleAccessMode, drive_mode: DriveAccessMode) -> Sequence[str]:
    scopes: list[str] = []
    scopes += list(SHEETS_SCOPES_READONLY if sheets_mode == "read" else SHEETS_SCOPES_READWRITE)

    if drive_mode == "read":
        scopes += list(DRIVE_SCOPES_READONLY)
    elif drive_mode == "write":
        scopes += list(DRIVE_SCOPES_FILE_WRITE)
    elif drive_mode == "all":
        scopes += list(DRIVE_SCOPES_ALL)
    elif drive_mode == "none":
        pass
    else:
        raise ValueError(f"Unsupported drive mode: {drive_mode}")

    # de-dupe while preserving order
    seen: set[str] = set()
    out: list[str] = []
    for s in scopes:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out
