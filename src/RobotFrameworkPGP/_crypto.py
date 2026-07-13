"""Encryption and decryption keywords for the PGP library."""

from typing import List, Optional, Union

from robot.api import logger
from robot.api.deco import keyword

from ._base import _Base


class EncryptionMixin(_Base):
    """Keywords for text/file encryption and decryption."""

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

        self._check_result(result, "Encryption")

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

        self._check_result(result, "Decryption")

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

        self._check_result(result, "File encryption")

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

        self._check_result(result, "File decryption")

        logger.info(f"Decrypted {input_file} to {output_file}")

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

        self._check_result(result, "Symmetric encryption")

        return str(result)
