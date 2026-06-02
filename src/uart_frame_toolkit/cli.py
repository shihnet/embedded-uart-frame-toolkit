from __future__ import annotations

import argparse
import json
import sys

from .frame import FrameError, decode_frame, encode_frame
from .profile import ProfileError, load_profile, render_markdown_table
from .smoke import SmokeTestError, dry_run_smoke_test


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="uart-frame")
    subparsers = parser.add_subparsers(dest="command", required=True)

    encode_parser = subparsers.add_parser("encode", help="encode a UART frame")
    encode_parser.add_argument("--cmd", required=True, help="command byte, e.g. 0x22")
    encode_parser.add_argument("--payload", default="", help="payload bytes, e.g. '01 02 03'")

    decode_parser = subparsers.add_parser("decode", help="decode a UART frame")
    decode_parser.add_argument("frame", help="frame bytes, e.g. '55 AA 22 00 22'")

    render_parser = subparsers.add_parser("render-profile", help="render a JSON profile as Markdown")
    render_parser.add_argument("profile", help="path to a public-safe JSON protocol profile")

    smoke_parser = subparsers.add_parser("smoke-test", help="build and validate a smoke-test frame")
    smoke_parser.add_argument("--cmd", required=True, help="request command byte, e.g. 0x42")
    smoke_parser.add_argument("--payload", default="", help="request payload bytes, e.g. '01 02'")
    smoke_parser.add_argument("--dry-run", action="store_true", help="build request without opening a port")
    smoke_parser.add_argument("--response", help="optional response frame bytes to validate")
    smoke_parser.add_argument("--expect-cmd", help="optional expected response command byte")

    args = parser.parse_args(argv)

    try:
        if args.command == "encode":
            cmd = _parse_byte(args.cmd)
            payload = _parse_bytes(args.payload)
            print(_format_hex(encode_frame(cmd, payload)))
            return 0

        if args.command == "decode":
            frame = decode_frame(_parse_bytes(args.frame))
            print(json.dumps(frame.as_dict(), separators=(",", ":")))
            return 0

        if args.command == "render-profile":
            rendered = render_markdown_table(load_profile(args.profile))
            print(rendered, end="")
            return 0

        if not args.dry_run:
            raise SmokeTestError("only --dry-run is supported until a serial backend is added")
        expected_cmd = _parse_byte(args.expect_cmd) if args.expect_cmd else None
        result = dry_run_smoke_test(
            _parse_byte(args.cmd),
            _parse_bytes(args.payload),
            _parse_bytes(args.response) if args.response else None,
            expected_cmd,
        )
        print(json.dumps(result.as_dict(), separators=(",", ":")))
        return 0
    except (FrameError, ProfileError, SmokeTestError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


def _parse_bytes(text: str) -> bytes:
    cleaned = text.replace(",", " ").strip()
    if not cleaned:
        return b""
    return bytes(_parse_byte(part) for part in cleaned.split())


def _parse_byte(text: str) -> int:
    token = text.strip()
    base = 16 if token.lower().startswith("0x") or _looks_like_hex_token(token) else 10
    try:
        value = int(token, base)
    except ValueError as exc:
        raise FrameError(f"invalid byte value: {text}") from exc
    if not 0 <= value <= 0xFF:
        raise FrameError(f"byte out of range: {text}")
    return value


def _looks_like_hex_token(text: str) -> bool:
    return len(text) == 2 and all(char in "0123456789abcdefABCDEF" for char in text)


def _format_hex(data: bytes) -> str:
    return " ".join(f"{byte:02X}" for byte in data)


if __name__ == "__main__":
    raise SystemExit(main())
