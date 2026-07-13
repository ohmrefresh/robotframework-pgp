"""Informational keywords for the PGP library."""

from typing import Any, Dict

from robot.api.deco import keyword

from ._base import _Base


class InfoMixin(_Base):
    """Keywords for querying GPG and key information."""

    @keyword
    def get_gpg_version(self) -> str:
        """Get the GPG version information.

        Returns:
            GPG version string

        Example:
            | ${version} | Get GPG Version |
        """
        # Different versions of python-gnupg may have different version attributes
        if hasattr(self._gpg, "version"):
            return str(self._gpg.version)
        elif hasattr(self._gpg, "binary_version"):
            return str(self._gpg.binary_version)
        else:
            # Fallback - try to get version info directly
            try:
                import subprocess

                result = subprocess.run(
                    ["gpg", "--version"], capture_output=True, text=True
                )
                return (
                    result.stdout.split("\n")[0]
                    if result.returncode == 0
                    else "Unknown"
                )
            except Exception:
                return "Unknown"

    @keyword
    def get_key_info(self, key_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific key.

        Args:
            key_id: Key ID, fingerprint, or email address

        Returns:
            Dictionary with key information

        Example:
            | ${info} | Get Key Info | test@example.com |
        """
        keys = self._gpg.list_keys()
        for key in keys:
            if self._key_matches(key_id, key):
                return {
                    "fingerprint": key.get("fingerprint", ""),
                    "keyid": key.get("keyid", ""),
                    "uids": key.get("uids", []),
                    "length": key.get("length", ""),
                    "algo": key.get("algo", ""),
                    "expires": key.get("expires", ""),
                    "trust": key.get("trust", ""),
                    "date": key.get("date", ""),
                    "subkeys": key.get("subkeys", []),
                }

        raise RuntimeError(f"Key not found: {key_id}")
