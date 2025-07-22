# Robot Framework PGP Library

A Robot Framework library for PGP/GPG encryption and decryption operations.

## Features

- PGP/GPG encryption and decryption
- Key generation and management
- Digital signatures
- Support for both symmetric and asymmetric encryption
- Easy integration with Robot Framework test suites

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
    ${encrypted}    Encrypt Text    Hello World    recipient@example.com
    ${decrypted}    Decrypt Text    ${encrypted}    passphrase=mypassword
    Should Be Equal    ${decrypted}    Hello World
```

## Documentation

Full documentation is available at [Read the Docs](https://robotframework-pgp.readthedocs.io/).

## Development

### Setup Development Environment

```bash
git clone https://github.com/robotframework/robotframework-pgp.git
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