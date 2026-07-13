"""Key management keywords for the PGP library."""

from typing import Any, Dict, List, Optional

from robot.api import logger
from robot.api.deco import keyword

from ._base import _Base


class KeyManagementMixin(_Base):
    """Keywords for generating, importing, exporting, listing, and deleting keys."""

    @keyword
    def generate_key_pair(
        self,
        email: str,
        name: str,
        key_length: int = 2048,
        passphrase: Optional[str] = None,
        expire_date: str = "0",
    ) -> str:
        """Generate a new GPG key pair.

        Args:
            email: Email address for the key
            name: Name for the key
            key_length: Key length in bits (default: 2048)
            passphrase: Passphrase to protect the private key
            expire_date: Expiration date (0 for no expiration)

        Returns:
            Key fingerprint of the generated key

        Example:
            | ${fingerprint} | Generate Key Pair | test@example.com | Test User | 2048 | secret123 |
        """
        input_data = self._gpg.gen_key_input(
            key_type="RSA",
            key_length=key_length,
            name_real=name,
            name_email=email,
            expire_date=expire_date,
            passphrase=passphrase or "",
        )

        key = self._gpg.gen_key(input_data)
        if not key:
            raise RuntimeError(f"Failed to generate key pair for {email}")

        logger.info(
            f"Generated key pair for {email} with fingerprint: {key.fingerprint}"
        )
        return str(key.fingerprint)

    @keyword
    def import_key(self, key_data: str) -> List[str]:
        """Import a GPG key from key data.

        Args:
            key_data: The key data to import (ASCII armored)

        Returns:
            List of imported key fingerprints

        Example:
            | ${fingerprints} | Import Key | ${key_data} |
        """
        result = self._gpg.import_keys(key_data)
        if result.count == 0:
            raise RuntimeError("Failed to import any keys")

        fingerprints = [fp for fp in result.fingerprints if fp]
        logger.info(f"Imported {len(fingerprints)} key(s): {fingerprints}")
        return fingerprints

    @keyword
    def import_key_from_file(self, key_file_path: str) -> List[str]:
        """Import a GPG key from a file.

        Args:
            key_file_path: Path to the key file

        Returns:
            List of imported key fingerprints

        Example:
            | ${fingerprints} | Import Key From File | /path/to/public.key |
        """
        with open(key_file_path, "r", encoding="utf-8") as f:
            key_data = f.read()
        return self.import_key(key_data)

    @keyword
    def export_public_key(self, key_id: str) -> str:
        """Export a public key.

        Args:
            key_id: Key ID, fingerprint, or email address

        Returns:
            ASCII armored public key

        Example:
            | ${public_key} | Export Public Key | test@example.com |
        """
        public_key = self._gpg.export_keys(key_id)
        if not public_key:
            raise RuntimeError(f"Failed to export public key for {key_id}")
        return str(public_key)

    @keyword
    def export_private_key(self, key_id: str, passphrase: Optional[str] = None) -> str:
        """Export a private key.

        Args:
            key_id: Key ID, fingerprint, or email address
            passphrase: Passphrase to unlock the private key

        Returns:
            ASCII armored private key

        Example:
            | ${private_key} | Export Private Key | test@example.com | secret123 |
        """
        private_key = self._gpg.export_keys(key_id, secret=True, passphrase=passphrase)
        if not private_key:
            raise RuntimeError(f"Failed to export private key for {key_id}")
        return str(private_key)

    @keyword
    def list_keys(self, secret: bool = False) -> List[Dict[str, Any]]:
        """List GPG keys.

        Args:
            secret: If True, list secret keys; otherwise list public keys

        Returns:
            List of key information dictionaries

        Example:
            | ${keys} | List Keys |
            | ${secret_keys} | List Keys | secret=${True} |
        """
        keys = self._gpg.list_keys(secret=secret)
        key_list = []
        for key in keys:
            key_info = {
                "fingerprint": key["fingerprint"],
                "keyid": key["keyid"],
                "uids": key["uids"],
                "length": key["length"],
                "algo": key["algo"],
                "expires": key["expires"],
                "trust": key.get("trust", ""),
            }
            key_list.append(key_info)
        return key_list

    @keyword
    def delete_key(
        self, key_id: str, secret: bool = False, passphrase: Optional[str] = None
    ) -> None:
        """Delete a GPG key.

        Args:
            key_id: Key ID, fingerprint, or email address
            secret: If True, delete secret key; otherwise delete public key
            passphrase: Passphrase to unlock the private key (for secret key deletion)

        Example:
            | Delete Key | test@example.com |
            | Delete Key | test@example.com | secret=${True} | passphrase=secret |
        """
        # Check if secret key exists first
        secret_keys = self._gpg.list_keys(secret=True)
        has_secret_key = any(self._key_matches(key_id, key) for key in secret_keys)

        if secret:
            # Delete secret key only
            result = self._gpg.delete_keys(key_id, secret=True, passphrase=passphrase)
        elif has_secret_key:
            # The secret key must be deleted before the public key; gpg does
            # not remove the public key when deleting the secret one.
            result = self._gpg.delete_keys(key_id, secret=True, passphrase=passphrase)
            result = self._gpg.delete_keys(key_id, secret=False)
        else:
            # Just delete public key
            result = self._gpg.delete_keys(key_id, secret=False)

        # Debug: Print result details
        logger.info(f"Delete result type: {type(result)}")
        if hasattr(result, "status"):
            logger.info(f"Delete status: {result.status}")
        if hasattr(result, "stderr"):
            logger.info(f"Delete stderr: {result.stderr}")
        if hasattr(result, "__dict__"):
            logger.info(f"Delete result attributes: {result.__dict__}")

        # Check if deletion was actually successful by verifying key no longer exists
        remaining_keys = self._gpg.list_keys()
        remaining_secret_keys = self._gpg.list_keys(secret=True)

        key_still_exists = any(self._key_matches(key_id, key) for key in remaining_keys)

        secret_key_still_exists = any(
            self._key_matches(key_id, key) for key in remaining_secret_keys
        )

        if secret and secret_key_still_exists:
            error_msg = (
                getattr(result, "status", "")
                or getattr(result, "stderr", "")
                or "No error message"
            )
            if error_msg != "ok":
                raise RuntimeError(f"Secret key deletion failed: {error_msg}")
        elif not secret and key_still_exists:
            error_msg = (
                getattr(result, "status", "")
                or getattr(result, "stderr", "")
                or "No error message"
            )
            if error_msg != "ok":
                raise RuntimeError(f"Key deletion failed: {error_msg}")
        logger.info(f"Deleted {'secret' if secret else 'public'} key: {key_id}")
