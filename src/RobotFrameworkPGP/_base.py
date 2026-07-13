"""Shared GPG state, lifecycle, and helpers for the PGP library mixins."""

import os
import shutil
import tempfile
from typing import Any, Dict, Optional

import gnupg  # type: ignore[import-untyped]
from robot.api import logger
from robot.api.deco import keyword


class _Base:
    """GPG initialization, lifecycle, and shared helper methods."""

    def __init__(self, gnupg_home: Optional[str] = None):
        """Initialize the PGP library.

        Args:
            gnupg_home: Optional path to GPG home directory. If not provided,
                       a temporary directory will be created.
        """
        self._gpg: gnupg.GPG
        self._gnupg_home = gnupg_home
        self._temp_dir: Optional[str] = None
        self._initialize_gpg()

    def _initialize_gpg(self) -> None:
        """Initialize GPG instance."""
        if self._gnupg_home:
            gnupg_home = self._gnupg_home
        else:
            self._temp_dir = tempfile.mkdtemp(prefix="robotframework_pgp_")
            gnupg_home = self._temp_dir

        os.makedirs(gnupg_home, exist_ok=True)
        # Configure GPG options for better batch mode support
        self._gpg = gnupg.GPG(
            gnupghome=gnupg_home,
            options=["--batch", "--yes", "--pinentry-mode", "loopback"],
        )
        logger.info(f"Initialized GPG with home directory: {gnupg_home}")

    def __del__(self) -> None:
        """Cleanup temporary directory if created."""
        if self._temp_dir and os.path.exists(self._temp_dir):
            shutil.rmtree(self._temp_dir, ignore_errors=True)

    @keyword
    def set_gpg_home_directory(self, gnupg_home: str) -> None:
        """Set the GPG home directory.

        Args:
            gnupg_home: Path to the GPG home directory.

        Example:
            | Set GPG Home Directory | /tmp/my_gnupg |
        """
        self._gnupg_home = gnupg_home
        self._initialize_gpg()

    @staticmethod
    def _check_result(result: Any, action: str) -> None:
        """Raise RuntimeError if a GPG operation result is not ok."""
        if not result.ok:
            raise RuntimeError(f"{action} failed: {result.status}")

    @staticmethod
    def _key_matches(key_id: str, key: Dict[str, Any]) -> bool:
        """Check whether key_id matches a key's fingerprint, keyid, or any UID."""
        return (
            key_id == key.get("fingerprint", "")
            or key_id == key.get("keyid", "")
            or any(key_id in uid for uid in key.get("uids", []))
        )
