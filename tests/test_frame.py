import unittest
from contextlib import redirect_stdout
from io import StringIO

from uart_frame_toolkit.cli import main
from uart_frame_toolkit import FrameError, decode_frame, encode_frame


class FrameTest(unittest.TestCase):
    def test_encode_frame(self):
        self.assertEqual(
            encode_frame(0x22, bytes([0x01, 0x02, 0x03])),
            bytes([0x55, 0xAA, 0x22, 0x03, 0x01, 0x02, 0x03, 0x2B]),
        )

    def test_decode_frame(self):
        frame = decode_frame(bytes([0x55, 0xAA, 0x42, 0x00, 0x42]))
        self.assertEqual(frame.cmd, 0x42)
        self.assertEqual(frame.payload, b"")
        self.assertEqual(frame.checksum, 0x42)

    def test_reject_bad_checksum(self):
        with self.assertRaises(FrameError):
            decode_frame(bytes([0x55, 0xAA, 0x42, 0x00, 0x00]))

    def test_reject_length_mismatch(self):
        with self.assertRaises(FrameError):
            decode_frame(bytes([0x55, 0xAA, 0x22, 0x02, 0x01, 0x23]))

    def test_cli_accepts_plain_hex_bytes(self):
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["decode", "55 AA 22 03 01 02 03 2B"]), 0)
        self.assertIn('"cmd":34', output.getvalue())


if __name__ == "__main__":
    unittest.main()
