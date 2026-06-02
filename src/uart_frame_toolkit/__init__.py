"""Utilities for encoding and decoding simple embedded UART frames."""

from .frame import Frame, FrameError, decode_frame, encode_frame

__all__ = ["Frame", "FrameError", "decode_frame", "encode_frame"]
