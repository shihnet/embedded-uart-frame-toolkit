# Embedded UART Frame Toolkit

A small, dependency-light Python toolkit for encoding and decoding framed UART
messages used in embedded bring-up, QA tools, and protocol documentation.

This project is intentionally generic. It does not include vendor firmware,
customer data, private register maps, or product-specific command tables.

## Frame Format

The default frame format is:

```text
55 AA CMD LEN PAYLOAD... CHECKSUM
```

- `55 AA`: start-of-frame bytes
- `CMD`: one-byte command ID
- `LEN`: payload byte count
- `PAYLOAD`: zero or more data bytes
- `CHECKSUM`: low 8 bits of `CMD + LEN + sum(PAYLOAD)`

## Install

```bash
python3 -m pip install .
```

For local development:

```bash
python3 -m pip install -e .
PYTHONPATH=src python3 -m unittest discover -s tests
```

## CLI Usage

Encode a frame:

```bash
uart-frame encode --cmd 0x22 --payload "01 02 03"
```

Decode a frame:

```bash
uart-frame decode "55 AA 22 03 01 02 03 2B"
```

Expected output:

```json
{"cmd":34,"payload":[1,2,3],"checksum":43}
```

More examples are available in [examples/basic-frames.md](examples/basic-frames.md).

## Why This Exists

Embedded teams often need a quick, auditable way to:

- verify UART frame construction
- reproduce QA-tool transactions
- document command examples
- build small protocol smoke tests

This toolkit provides a simple baseline that maintainers can extend with
project-specific protocol profiles without exposing proprietary firmware.

## Roadmap

- Add named protocol profiles from public specs
- Add serial-port smoke-test helpers
- Add Markdown protocol table generation
- Add CI examples for firmware-adjacent repositories

## License

MIT
