"""Utilities for encoding and decoding simple embedded UART frames."""

from .frame import Frame, FrameError, decode_frame, encode_frame
from .profile import ProfileError, load_profile, render_markdown_table

__all__ = [
    "Frame",
    "FrameError",
    "ProfileError",
    "decode_frame",
    "encode_frame",
    "load_profile",
    "render_markdown_table",
]
