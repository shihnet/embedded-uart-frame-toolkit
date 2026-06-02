from __future__ import annotations

from dataclasses import dataclass

from .frame import Frame, FrameError, decode_frame, encode_frame


class SmokeTestError(ValueError):
    """Raised when a smoke-test request or response is invalid."""


@dataclass(frozen=True)
class SmokeTestResult:
    request: bytes
    response: Frame | None
    status: str

    def as_dict(self) -> dict[str, object]:
        data: dict[str, object] = {
            "request": _format_hex(self.request),
            "status": self.status,
        }
        if self.response is not None:
            data["response"] = self.response.as_dict()
        return data


def build_smoke_request(cmd: int, payload: bytes = b"") -> bytes:
    return encode_frame(cmd, payload)


def dry_run_smoke_test(
    cmd: int,
    payload: bytes = b"",
    response: bytes | None = None,
    expected_response_cmd: int | None = None,
) -> SmokeTestResult:
    request = build_smoke_request(cmd, payload)
    if response is None:
        return SmokeTestResult(request=request, response=None, status="request-ready")

    try:
        decoded = decode_frame(response)
    except FrameError as exc:
        raise SmokeTestError(f"invalid response frame: {exc}") from exc

    if expected_response_cmd is not None and decoded.cmd != expected_response_cmd:
        raise SmokeTestError(
            f"unexpected response command: expected 0x{expected_response_cmd:02X}, "
            f"got 0x{decoded.cmd:02X}"
        )

    return SmokeTestResult(request=request, response=decoded, status="response-ok")


def _format_hex(data: bytes) -> str:
    return " ".join(f"{byte:02X}" for byte in data)
