# Protocol Profile Format

`uart-frame render-profile` accepts a JSON file and renders a Markdown command
table.

The profile format is intentionally small and public-safe. It is for examples,
documentation, and smoke-test profiles. Do not add proprietary command tables,
customer data, private register maps, or production-only procedures.

## Example

```json
{
  "title": "Example Public UART Profile",
  "description": "A small public-safe example profile for documentation generation.",
  "commands": [
    {
      "cmd": "0x22",
      "name": "Read version",
      "payload": "-",
      "response": "ASCII version string",
      "notes": "Useful for smoke testing host-tool connectivity."
    }
  ]
}
```

## Fields

Top-level fields:

| Field | Required | Description |
| --- | --- | --- |
| `title` | No | Markdown document title. Defaults to `Protocol Profile`. |
| `description` | No | Short paragraph shown before the table. |
| `commands` | Yes | Non-empty command array. |

Command fields:

| Field | Required | Description |
| --- | --- | --- |
| `cmd` | Yes | Command byte as an integer or string, such as `66` or `"0x42"`. |
| `name` | No | Human-readable command name. |
| `payload` | No | Public-safe payload description. Defaults to `-`. |
| `response` | No | Public-safe response description. Defaults to `-`. |
| `notes` | No | Public-safe implementation or usage note. |

## CLI

```bash
uart-frame render-profile examples/public-profile.json
```

For local development without installing the package:

```bash
PYTHONPATH=src python3 -m uart_frame_toolkit.cli render-profile examples/public-profile.json
```
