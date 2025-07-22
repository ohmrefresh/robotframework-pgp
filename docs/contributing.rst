Contributing
============

We welcome contributions to the Robot Framework PGP library! This document provides guidelines for contributing to the project.

Getting Started
---------------

1. **Fork the Repository**

   Fork the repository on GitHub and clone your fork:

   .. code-block:: bash

      git clone https://github.com/yourusername/robotframework-pgp.git
      cd robotframework-pgp

2. **Set Up Development Environment**

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate
      pip install -r requirements-dev.txt
      pip install -e .

3. **Install Pre-commit Hooks**

   .. code-block:: bash

      pre-commit install

Development Workflow
--------------------

1. **Create a Branch**

   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. **Make Changes**

   - Write your code following the project's coding standards
   - Add or update tests for your changes
   - Update documentation if necessary

3. **Run Tests**

   .. code-block:: bash

      # Run unit tests
      pytest

      # Run Robot Framework tests
      robot tests/acceptance/

      # Run with coverage
      pytest --cov=RobotFrameworkPGP

4. **Code Quality Checks**

   .. code-block:: bash

      # Format code
      black src/ tests/

      # Lint code
      flake8 src/ tests/

      # Type checking
      mypy src/

5. **Commit and Push**

   .. code-block:: bash

      git add .
      git commit -m "Add feature: description of your changes"
      git push origin feature/your-feature-name

6. **Create Pull Request**

   Create a pull request on GitHub with a clear description of your changes.

Coding Standards
----------------

**Python Code Style**

- Follow PEP 8 style guide
- Use Black for code formatting
- Maximum line length: 88 characters
- Use type hints for function parameters and return values

**Robot Framework Code Style**

- Use 4 spaces for indentation
- Use clear, descriptive test and keyword names
- Follow Robot Framework best practices

**Documentation**

- Use Google-style docstrings for Python functions
- Update RST documentation for new features
- Include examples in docstrings

Testing Guidelines
------------------

**Unit Tests**

- Write comprehensive unit tests for all new functionality
- Use pytest fixtures for setup and teardown
- Aim for high test coverage (>90%)
- Test both success and failure scenarios

**Integration Tests**

- Create Robot Framework test cases for new keywords
- Test realistic usage scenarios
- Verify error handling and edge cases

**Test Structure**

.. code-block:: text

   tests/
   ├── __init__.py
   ├── conftest.py              # Pytest configuration
   ├── test_pgp_library.py      # Unit tests
   └── acceptance/              # Robot Framework tests
       ├── basic_encryption.robot
       ├── file_encryption.robot
       └── advanced_features.robot

Documentation
-------------

**Updating Documentation**

When adding new features:

1. Update keyword documentation in the source code
2. Add examples to the appropriate documentation files
3. Update the API reference if needed
4. Test documentation builds locally:

   .. code-block:: bash

      cd docs
      make html

**Documentation Structure**

.. code-block:: text

   docs/
   ├── conf.py              # Sphinx configuration
   ├── index.rst           # Main documentation page
   ├── installation.rst    # Installation guide
   ├── quickstart.rst      # Quick start guide
   ├── examples.rst        # Usage examples
   ├── keywords.rst        # Keyword reference
   ├── api.rst            # API documentation
   └── contributing.rst    # This file

Reporting Issues
----------------

When reporting issues:

1. Use the GitHub issue tracker
2. Provide a clear description of the problem
3. Include steps to reproduce the issue
4. Specify your environment (OS, Python version, GPG version)
5. Include relevant logs or error messages

Feature Requests
----------------

For new features:

1. Check existing issues to avoid duplicates
2. Describe the use case and benefits
3. Propose an API design if applicable
4. Be open to discussion and feedback

Release Process
---------------

**Version Numbering**

We follow Semantic Versioning (SemVer):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

**Release Steps**

1. Update version in ``pyproject.toml`` and ``__init__.py``
2. Update ``CHANGELOG.md`` with release notes
3. Create and push a version tag:

   .. code-block:: bash

      git tag v1.2.3
      git push origin v1.2.3

4. GitHub Actions will automatically build and publish to PyPI

Code Review Guidelines
----------------------

**For Contributors**

- Keep pull requests focused and reasonably sized
- Write clear commit messages
- Respond to review feedback promptly
- Update your branch with the latest main branch changes

**For Reviewers**

- Be constructive and respectful in feedback
- Check code quality, tests, and documentation
- Verify that changes don't break existing functionality
- Consider the impact on users and backward compatibility

Community
---------

**Communication**

- GitHub Discussions for questions and general discussion
- GitHub Issues for bug reports and feature requests
- Follow the project's code of conduct

**Getting Help**

If you need help with development:

1. Check existing documentation and examples
2. Search GitHub issues for similar problems
3. Ask questions in GitHub Discussions
4. Join the Robot Framework community forums

Thank you for contributing to Robot Framework PGP!