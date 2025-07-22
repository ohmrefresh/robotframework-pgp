"""Main Robot Framework PGP Library implementation."""

import os
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Union, List, Dict, Any
import gnupg
from robot.api.deco import keyword, library
from robot.api import logger
from robot.utils import ConnectionCache


@library(scope="GLOBAL", doc_format="ROBOT")
class RobotFrameworkPGP:
    """Robot Framework library for PGP/GPG encryption and decryption operations.

    This library provides keywords for:
    - Text and file encryption/decryption
    - Key generation and management
    - Digital signatures
    - GPG operations

    = Table of contents =

    - `Initialization`
    - `Configuration`
    - `Encryption and Decryption`
    - `Key Management`
    - `Digital Signatures`
    - `Utility Keywords`

    = Initialization =

    The library can be imported with optional parameters:

    | Library | RobotFrameworkPGP |
    | Library | RobotFrameworkPGP | gnupg_home=/path/to/gnupg |

    = Configuration =

    Before using encryption/decryption operations, you need to configure the GPG environment.

    = Examples =

    | `Set GPG Home Directory` | /tmp/gnupg |
    | `Generate Key Pair` | test@example.com | Test User | 2048 |
    | ${encrypted} | `Encrypt Text` | Hello World | test@example.com |
    | ${decrypted} | `Decrypt Text` | ${encrypted} | passphrase=secret |
    """

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_VERSION = "1.0.0"
    ROBOT_LIBRARY_DOC_FORMAT = "ROBOT"

    def __init__(self, gnupg_home: Optional[str] = None):
        """Initialize the PGP library.

        Args:
            gnupg_home: Optional path to GPG home directory. If not provided,
                       a temporary directory will be created.
        """
        self._gpg = None
        self._gnupg_home = gnupg_home
        self._temp_dir = None
        self._initialize_gpg()

    def _initialize_gpg(self):
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

    def __del__(self):
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
        return public_key

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
        return private_key

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
    def encrypt_text(
        self,
        text: str,
        recipients: Union[str, List[str]],
        sign: Optional[str] = None,
        passphrase: Optional[str] = None,
        armor: bool = True,
    ) -> str:
        """Encrypt text for specified recipients.

        Args:
            text: Text to encrypt
            recipients: Recipient key ID(s), fingerprint(s), or email address(es)
            sign: Optional key ID to sign with
            passphrase: Passphrase for signing key
            armor: If True, return ASCII armored output

        Returns:
            Encrypted text

        Example:
            | ${encrypted} | Encrypt Text | Hello World | test@example.com |
            | ${encrypted} | Encrypt Text | Secret message | test@example.com | sign=signer@example.com | passphrase=secret |
        """
        if isinstance(recipients, str):
            recipients = [recipients]

        result = self._gpg.encrypt(
            text, recipients, sign=sign, passphrase=passphrase, armor=armor
        )

        if not result.ok:
            raise RuntimeError(f"Encryption failed: {result.status}")

        return str(result)

    @keyword
    def decrypt_text(
        self, encrypted_text: str, passphrase: Optional[str] = None
    ) -> str:
        """Decrypt encrypted text.

        Args:
            encrypted_text: Encrypted text to decrypt
            passphrase: Passphrase to unlock the private key

        Returns:
            Decrypted text

        Example:
            | ${decrypted} | Decrypt Text | ${encrypted_text} | passphrase=secret |
        """
        result = self._gpg.decrypt(encrypted_text, passphrase=passphrase)

        if not result.ok:
            raise RuntimeError(f"Decryption failed: {result.status}")

        return str(result)

    @keyword
    def encrypt_file(
        self,
        input_file: str,
        output_file: str,
        recipients: Union[str, List[str]],
        sign: Optional[str] = None,
        passphrase: Optional[str] = None,
        armor: bool = True,
    ) -> None:
        """Encrypt a file for specified recipients.

        Args:
            input_file: Path to the input file
            output_file: Path to the output encrypted file
            recipients: Recipient key ID(s), fingerprint(s), or email address(es)
            sign: Optional key ID to sign with
            passphrase: Passphrase for signing key
            armor: If True, create ASCII armored output

        Example:
            | Encrypt File | input.txt | output.txt.gpg | test@example.com |
        """
        if isinstance(recipients, str):
            recipients = [recipients]

        with open(input_file, "rb") as f:
            result = self._gpg.encrypt_file(
                f,
                recipients,
                sign=sign,
                passphrase=passphrase,
                armor=armor,
                output=output_file,
            )

        if not result.ok:
            raise RuntimeError(f"File encryption failed: {result.status}")

        logger.info(f"Encrypted {input_file} to {output_file}")

    @keyword
    def decrypt_file(
        self, input_file: str, output_file: str, passphrase: Optional[str] = None
    ) -> None:
        """Decrypt an encrypted file.

        Args:
            input_file: Path to the encrypted input file
            output_file: Path to the decrypted output file
            passphrase: Passphrase to unlock the private key

        Example:
            | Decrypt File | input.txt.gpg | output.txt | passphrase=secret |
        """
        with open(input_file, "rb") as f:
            result = self._gpg.decrypt_file(
                f, passphrase=passphrase, output=output_file
            )

        if not result.ok:
            raise RuntimeError(f"File decryption failed: {result.status}")

        logger.info(f"Decrypted {input_file} to {output_file}")

    @keyword
    def sign_text(
        self, text: str, key_id: str, passphrase: Optional[str] = None
    ) -> str:
        """Create a digital signature for text.

        Args:
            text: Text to sign
            key_id: Key ID, fingerprint, or email address to sign with
            passphrase: Passphrase to unlock the private key

        Returns:
            Signed text (cleartext signature)

        Example:
            | ${signed} | Sign Text | Hello World | test@example.com | passphrase=secret |
        """
        result = self._gpg.sign(text, keyid=key_id, passphrase=passphrase)

        if not result:
            raise RuntimeError(f"Text signing failed")

        return str(result)

    @keyword
    def verify_signature(self, signed_text: str) -> Dict[str, Any]:
        """Verify a digital signature.

        Args:
            signed_text: Signed text to verify

        Returns:
            Dictionary with verification results

        Example:
            | ${result} | Verify Signature | ${signed_text} |
            | Should Be True | ${result}[valid] |
        """
        result = self._gpg.verify(signed_text)

        verification_result = {
            "valid": result.valid,
            "fingerprint": result.fingerprint,
            "key_id": result.key_id,
            "username": result.username,
            "trust_level": result.trust_level,
            "trust_text": result.trust_text,
            "signature_id": result.signature_id,
            "timestamp": result.timestamp,
        }

        return verification_result

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
        has_secret_key = any(
            key_id == key.get("fingerprint", "")
            or key_id == key.get("keyid", "")
            or any(key_id in uid for uid in key.get("uids", []))
            for key in secret_keys
        )

        if secret:
            # Delete secret key only
            result = self._gpg.delete_keys(key_id, secret=True, passphrase=passphrase)
        elif has_secret_key:
            # Delete secret key first (this should also remove the public key)
            result = self._gpg.delete_keys(key_id, secret=True, passphrase=passphrase)
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

        key_still_exists = any(
            key_id == key.get("fingerprint", "")
            or key_id == key.get("keyid", "")
            or any(key_id in uid for uid in key.get("uids", []))
            for key in remaining_keys
        )

        secret_key_still_exists = any(
            key_id == key.get("fingerprint", "")
            or key_id == key.get("keyid", "")
            or any(key_id in uid for uid in key.get("uids", []))
            for key in remaining_secret_keys
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
            return self._gpg.version
        elif hasattr(self._gpg, "binary_version"):
            return self._gpg.binary_version
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
            except:
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
            # Check if key_id matches any of the key identifiers
            key_match = False

            # Check fingerprint
            if key_id == key.get("fingerprint", ""):
                key_match = True
            # Check keyid
            elif key_id == key.get("keyid", ""):
                key_match = True
            # Check if key_id is in any of the UIDs
            elif key.get("uids"):
                for uid in key["uids"]:
                    if key_id in uid:
                        key_match = True
                        break

            if key_match:
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

    @keyword
    def create_symmetric_encryption(self, text: str, passphrase: str) -> str:
        """Create symmetric encryption (password-based).

        Args:
            text: Text to encrypt
            passphrase: Passphrase for encryption

        Returns:
            Encrypted text

        Example:
            | ${encrypted} | Create Symmetric Encryption | Secret data | mypassword |
        """
        result = self._gpg.encrypt(
            text, recipients=None, symmetric=True, passphrase=passphrase
        )

        if not result.ok:
            raise RuntimeError(f"Symmetric encryption failed: {result.status}")

        return str(result)
