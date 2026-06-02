# Contributing

Contributions are welcome when they keep the project generic, testable, and
safe to publish.

## Scope

Good contributions include:

- generic UART frame parsing improvements
- CLI usability fixes
- public protocol profile examples
- documentation and test improvements
- CI and release workflow improvements

Out of scope:

- proprietary firmware source
- customer-specific command tables
- private register maps or factory procedures
- credentials, serial numbers, or production logs

## Development

Run the test suite before opening a pull request:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

Keep new parser behavior covered by tests. Prefer small changes that are easy
to review.

## Issue Reports

When reporting a bug, include:

- command used
- expected output
- actual output
- Python version
- minimal frame data needed to reproduce the issue

Do not include private device data or confidential protocol definitions.
