"""Digital signature keywords for the PGP library."""

from typing import Any, Dict, Optional

from robot.api.deco import keyword

from ._base import _Base


class SigningMixin(_Base):
    """Keywords for creating and verifying digital signatures."""

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
            raise RuntimeError("Text signing failed")

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
