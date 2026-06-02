from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class ProfileError(ValueError):
    """Raised when a protocol profile cannot be rendered."""


@dataclass(frozen=True)
class CommandProfile:
    cmd: int
    name: str
    payload: str
    response: str
    notes: str


def load_profile(path: str | Path) -> dict[str, Any]:
    try:
        raw = Path(path).read_text(encoding="utf-8")
        data = json.loads(raw)
    except OSError as exc:
        raise ProfileError(f"cannot read profile: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ProfileError(f"invalid JSON profile: {exc}") from exc

    if not isinstance(data, dict):
        raise ProfileError("profile root must be a JSON object")
    return data


def render_markdown_table(profile: dict[str, Any]) -> str:
    title = _string_field(profile, "title", "Protocol Profile")
    description = _string_field(profile, "description", "")
    commands_raw = profile.get("commands")
    if not isinstance(commands_raw, list) or not commands_raw:
        raise ProfileError("profile must contain a non-empty commands array")

    commands = [_parse_command(item, index) for index, item in enumerate(commands_raw, start=1)]

    lines = [f"# {title}", ""]
    if description:
        lines.extend([description, ""])

    lines.extend(
        [
            "| Command | Name | Payload | Response | Notes |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for command in commands:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`0x{command.cmd:02X}`",
                    _escape_table_cell(command.name),
                    _escape_table_cell(command.payload),
                    _escape_table_cell(command.response),
                    _escape_table_cell(command.notes),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def _parse_command(item: Any, index: int) -> CommandProfile:
    if not isinstance(item, dict):
        raise ProfileError(f"commands[{index}] must be an object")
    return CommandProfile(
        cmd=_command_byte(item.get("cmd"), index),
        name=_string_field(item, "name", f"Command {index}"),
        payload=_string_field(item, "payload", "-"),
        response=_string_field(item, "response", "-"),
        notes=_string_field(item, "notes", ""),
    )


def _command_byte(value: Any, index: int) -> int:
    if isinstance(value, str):
        try:
            parsed = int(value, 0)
        except ValueError as exc:
            raise ProfileError(f"commands[{index}].cmd is not a byte value") from exc
    elif isinstance(value, int):
        parsed = value
    else:
        raise ProfileError(f"commands[{index}].cmd is required")

    if not 0 <= parsed <= 0xFF:
        raise ProfileError(f"commands[{index}].cmd must be in range 0x00..0xFF")
    return parsed


def _string_field(data: dict[str, Any], key: str, default: str) -> str:
    value = data.get(key, default)
    if value is None:
        return default
    if not isinstance(value, str):
        raise ProfileError(f"{key} must be a string")
    return value


def _escape_table_cell(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace("|", "\\|")
    return escaped.replace("\n", "<br>")
