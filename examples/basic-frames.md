# Basic Frame Examples

These examples use the default public-safe frame format:

```text
55 AA CMD LEN PAYLOAD... CHECKSUM
```

## Empty Payload

Command:

```bash
uart-frame encode --cmd 0x42
```

Frame:

```text
55 AA 42 00 42
```

Decoded:

```json
{"cmd":66,"payload":[],"checksum":66}
```

## Three-Byte Payload

Command:

```bash
uart-frame encode --cmd 0x22 --payload "01 02 03"
```

Frame:

```text
55 AA 22 03 01 02 03 2B
```

Decoded:

```json
{"cmd":34,"payload":[1,2,3],"checksum":43}
```

## Malformed Checksum

Input:

```bash
uart-frame decode "55 AA 42 00 00"
```

Expected behavior:

```text
error: checksum mismatch: expected 0x42, got 0x00
```
