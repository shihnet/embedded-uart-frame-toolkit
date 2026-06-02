# Security Policy

## Supported Versions

The latest released version is the supported version.

## Reporting a Vulnerability

Open a GitHub issue for non-sensitive parser robustness problems.

For sensitive reports, avoid posting private firmware, credentials, production
logs, customer identifiers, or confidential command tables. Share only the
minimal public-safe frame data needed to explain the issue.

## Parser Safety Notes

This project treats UART frame bytes as untrusted input. Changes that affect
decoding, length validation, checksum validation, or CLI parsing should include
unit tests for malformed input.
