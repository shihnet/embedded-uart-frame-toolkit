import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from uart_frame_toolkit import ProfileError, load_profile, render_markdown_table
from uart_frame_toolkit.cli import main


class ProfileTest(unittest.TestCase):
    def test_render_markdown_table(self):
        markdown = render_markdown_table(
            {
                "title": "Example Protocol",
                "description": "Public example profile.",
                "commands": [
                    {
                        "cmd": "0x22",
                        "name": "Read version",
                        "payload": "-",
                        "response": "ASCII version",
                        "notes": "Smoke-test command",
                    }
                ],
            }
        )

        self.assertIn("# Example Protocol", markdown)
        self.assertIn("| `0x22` | Read version | - | ASCII version | Smoke-test command |", markdown)

    def test_reject_empty_commands(self):
        with self.assertRaises(ProfileError):
            render_markdown_table({"commands": []})

    def test_reject_out_of_range_command(self):
        with self.assertRaises(ProfileError):
            render_markdown_table({"commands": [{"cmd": 0x100}]})

    def test_load_profile_and_cli_render(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            profile_path = Path(tmpdir) / "profile.json"
            profile_path.write_text(
                '{"title":"Demo","commands":[{"cmd":66,"name":"Ping"}]}',
                encoding="utf-8",
            )

            output = StringIO()
            self.assertEqual(load_profile(profile_path)["title"], "Demo")
            with redirect_stdout(output):
                self.assertEqual(main(["render-profile", str(profile_path)]), 0)
            self.assertIn("# Demo", output.getvalue())


if __name__ == "__main__":
    unittest.main()
