Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[Unreleased]
------------

[1.1.1] - 2026-07-13
---------------------

Fixed
~~~~~
- Example suites: ``${TEMP_DIR}`` variable collided with Robot Framework's built-in ``${TEMPDIR}`` (recursive definition), broken ``Suite Teardown`` wiring, and ``Delete Key`` usage on GnuPG >= 2.1
- Stale ``ROBOT_LIBRARY_VERSION`` reported by the library
- Broken ``Delete Key`` snippets in documentation

Added
~~~~~
- ``examples/key_management.robot`` with isolated GPG home, key inspection, and private key backup/restore examples
- Private key backup/restore and ``Import Key From File`` documentation

[1.1.0] - 2026-07-13
---------------------

Added
~~~~~
- Maintainer/author email and ``Framework :: Robot Framework`` classifier in package metadata
- CI workflow testing across multiple Robot Framework versions
- Key management and utility keyword examples (``examples/key_management.robot``)

Changed
~~~~~~~
- Release workflow now uses PyPI trusted publishing and triggers Read the Docs builds

Removed
~~~~~~~
- Unused ``cryptography`` dependency

[1.0.0] - 2024-01-01
---------------------

Added
~~~~~
- Initial release of Robot Framework PGP library
- Text encryption and decryption functionality
- File encryption and decryption functionality
- Digital signature creation and verification
- Key pair generation with customizable parameters
- Key import and export functionality
- Support for multiple recipients
- Symmetric encryption (password-based)
- Key management operations (list, delete, get info)
- Comprehensive error handling
- Full Robot Framework integration
- Complete documentation with examples
- Unit tests with pytest
- Integration tests with Robot Framework
- CI/CD pipeline with GitHub Actions
- PyPI package automation
- Read the Docs documentation

Security
~~~~~~~~
- Secure key generation with configurable key lengths
- Proper passphrase handling
- Temporary directory cleanup
- No sensitive data logging

Documentation
~~~~~~~~~~~~~
- Complete API documentation
- User guide with examples
- Installation instructions
- Contributing guidelines
- Keyword reference documentation

Testing
~~~~~~~
- Comprehensive unit test suite
- Robot Framework integration tests
- Test coverage reporting
- Automated testing in CI/CD pipeline

[0.1.0] - 2023-12-01
---------------------

Added
~~~~~
- Initial project structure
- Basic PGP functionality proof of concept
- Development environment setup