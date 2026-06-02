# GitHub and Application Checklist

## Already Prepared

- Public-safe OSS project concept
- Python package scaffold
- CLI command: `uart-frame`
- Unit tests
- README
- MIT license
- `.gitignore`
- Codex for Open Source application draft

## Local Verification

Run from the repository root:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 -m uart_frame_toolkit.cli encode --cmd 0x22 --payload "01 02 03"
PYTHONPATH=src python3 -m uart_frame_toolkit.cli decode "55 AA 22 03 01 02 03 2B"
```

Expected results:

- Unit tests pass
- Encode prints `55 AA 22 03 01 02 03 2B`
- Decode prints `{"cmd":34,"payload":[1,2,3],"checksum":43}`

## GitHub Steps

1. Create a public GitHub repository named `embedded-uart-frame-toolkit`.
2. Push this folder as the first commit.
3. Edit `pyproject.toml` author name.
4. Edit `LICENSE` copyright owner.
5. Add a short GitHub repository description.
6. Add topics: `embedded`, `uart`, `firmware`, `protocol`, `python`.
7. Create a first GitHub release tag, for example `v0.1.0`.
8. Open at least two issues:
   - Add serial-port smoke-test helper
   - Add Markdown protocol table generator
9. Add one roadmap item or project board if useful.

## Application Timing

Do not submit immediately after creating an empty repository. A stronger minimum
signal is:

- repo is public
- initial release exists
- README is complete
- tests pass
- at least a small maintenance trail exists, such as issues and follow-up commits

## Application Positioning

Be accurate. Do not claim the project is widely used unless there is real public
usage evidence.

A safer positioning is:

> I am starting and maintaining a public embedded tooling project that provides
> reusable UART frame parsing and documentation utilities. I am applying for
> Codex support to improve tests, parser safety, documentation generation, and
> maintainer workflows as the project grows.

## Risk Notes

- This does not guarantee acceptance.
- The project must remain free of private firmware, customer data, confidential
  command tables, and proprietary hardware details.
- Codex Security or API credits may require extra review.
