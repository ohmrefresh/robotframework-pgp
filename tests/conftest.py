"""Pytest configuration and fixtures."""

import pytest
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


@pytest.fixture(scope="session")
def gpg_available():
    """Check if GPG is available on the system."""
    import shutil

    return shutil.which("gpg") is not None


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "requires_gpg: mark test as requiring GPG binary"
    )


def pytest_collection_modifyitems(config, items):
    """Skip GPG tests if GPG is not available."""
    import shutil

    if shutil.which("gpg") is None:
        skip_gpg = pytest.mark.skip(reason="GPG binary not available")
        for item in items:
            if "test_" in item.nodeid:
                item.add_marker(skip_gpg)
