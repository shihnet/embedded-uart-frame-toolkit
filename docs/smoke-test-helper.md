# Smoke-Test Helper

`uart-frame smoke-test` helps prepare and validate generic smoke-test frames.

The current implementation is intentionally dry-run only. It does not open a
serial port and does not require `pyserial` or real hardware. This keeps the
project dependency-light while still allowing maintainers to verify frame
construction and expected response parsing.

## Build a Request

```bash
uart-frame smoke-test --dry-run --cmd 0x42
```

Output:

```json
{"request":"55 AA 42 00 42","status":"request-ready"}
```

## Validate a Response

```bash
uart-frame smoke-test --dry-run --cmd 0x42 --response "55 AA 42 00 42" --expect-cmd 0x42
```

Output:

```json
{"request":"55 AA 42 00 42","status":"response-ok","response":{"cmd":66,"payload":[],"checksum":66}}
```

## Future Serial Backend

A future optional serial backend can add real port handling without changing the
dry-run contract. That backend should remain optional and should not introduce
hardware-specific command tables.
