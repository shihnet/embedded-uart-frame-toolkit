import unittest
from contextlib import redirect_stdout
from io import StringIO

from uart_frame_toolkit import SmokeTestError, build_smoke_request, dry_run_smoke_test
from uart_frame_toolkit.cli import main


class SmokeTest(unittest.TestCase):
    def test_build_smoke_request(self):
        self.assertEqual(build_smoke_request(0x42), bytes([0x55, 0xAA, 0x42, 0x00, 0x42]))

    def test_dry_run_without_response(self):
        result = dry_run_smoke_test(0x42)
        self.assertEqual(result.status, "request-ready")
        self.assertIsNone(result.response)
        self.assertEqual(result.as_dict()["request"], "55 AA 42 00 42")

    def test_dry_run_with_response(self):
        result = dry_run_smoke_test(0x42, response=bytes([0x55, 0xAA, 0x42, 0x00, 0x42]))
        self.assertEqual(result.status, "response-ok")
        self.assertEqual(result.response.cmd, 0x42)

    def test_reject_unexpected_response_command(self):
        with self.assertRaises(SmokeTestError):
            dry_run_smoke_test(
                0x42,
                response=bytes([0x55, 0xAA, 0x22, 0x00, 0x22]),
                expected_response_cmd=0x42,
            )

    def test_cli_smoke_test_dry_run(self):
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["smoke-test", "--dry-run", "--cmd", "0x42"]), 0)
        self.assertIn('"status":"request-ready"', output.getvalue())


if __name__ == "__main__":
    unittest.main()
