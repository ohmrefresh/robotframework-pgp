# Robot Framework PGP Library

A Robot Framework library for PGP/GPG encryption and decryption operations.

## Features

- Text and file encryption/decryption (asymmetric and symmetric)
- Key generation, import/export (public and private), inspection, and deletion
- Digital signatures with cleartext signing and verification
- Isolated GPG home directory support for hermetic test runs
- 17 keywords, easy integration with Robot Framework test suites

## Requirements

- Python 3.8+
- A `gpg` binary on the PATH (GnuPG 2.x) — there is no pure-Python fallback

## Installation

```bash
pip install robotframework-pgp
```

## Quick Start

```robot
*** Settings ***
Library    RobotFrameworkPGP

*** Test Cases ***
Encrypt And Decrypt Text
    Generate Key Pair    recipient@example.com    Test User    2048    mypassword
    ${encrypted}    Encrypt Text    Hello World    recipient@example.com
    ${decrypted}    Decrypt Text    ${encrypted}    passphrase=mypassword
    Should Be Equal    ${decrypted}    Hello World
```

Runnable example suites live in [`examples/`](examples/): basic usage,
file operations, and key management.

## Documentation

Full documentation is available at [Read the Docs](https://robotframework-pgp.readthedocs.io/).

## Development

### Setup Development Environment

```bash
git clone https://github.com/ohmrefresh/robotframework-pgp.git
cd robotframework-pgp
pip install -r requirements-dev.txt
```

### Running Tests

```bash
pytest
```

### Running Robot Framework Tests

```bash
robot tests/acceptance/
```

## License

Apache License 2.0