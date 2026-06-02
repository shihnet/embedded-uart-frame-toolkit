from __future__ import annotations

from dataclasses import dataclass


SOF = bytes([0x55, 0xAA])


class FrameError(ValueError):
    """Raised when a UART frame cannot be parsed or validated."""


@dataclass(frozen=True)
class Frame:
    cmd: int
    payload: bytes
    checksum: int

    def as_dict(self) -> dict[str, object]:
        return {
            "cmd": self.cmd,
            "payload": list(self.payload),
            "checksum": self.checksum,
        }


def encode_frame(cmd: int, payload: bytes = b"") -> bytes:
    _validate_byte(cmd, "cmd")
    if len(payload) > 255:
        raise FrameError("payload length must fit in one byte")

    length = len(payload)
    checksum = _checksum(cmd, length, payload)
    return SOF + bytes([cmd, length]) + payload + bytes([checksum])


def decode_frame(data: bytes) -> Frame:
    if len(data) < 5:
        raise FrameError("frame is too short")
    if data[:2] != SOF:
        raise FrameError("invalid start-of-frame bytes")

    cmd = data[2]
    length = data[3]
    expected_size = 2 + 1 + 1 + length + 1
    if len(data) != expected_size:
        raise FrameError(f"frame length mismatch: expected {expected_size}, got {len(data)}")

    payload = data[4 : 4 + length]
    checksum = data[-1]
    expected_checksum = _checksum(cmd, length, payload)
    if checksum != expected_checksum:
        raise FrameError(
            f"checksum mismatch: expected 0x{expected_checksum:02X}, got 0x{checksum:02X}"
        )

    return Frame(cmd=cmd, payload=payload, checksum=checksum)


def _checksum(cmd: int, length: int, payload: bytes) -> int:
    return (cmd + length + sum(payload)) & 0xFF


def _validate_byte(value: int, name: str) -> None:
    if not 0 <= value <= 0xFF:
        raise FrameError(f"{name} must be in range 0x00..0xFF")
