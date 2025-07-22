"""Unit tests for RobotFrameworkPGP library."""

import os
import tempfile
import pytest
from pathlib import Path

from RobotFrameworkPGP import RobotFrameworkPGP


class TestRobotFrameworkPGP:
    """Test cases for RobotFrameworkPGP library."""

    @pytest.fixture
    def temp_gpg_home(self):
        """Create a temporary GPG home directory."""
        temp_dir = tempfile.mkdtemp(prefix="test_gpg_")
        yield temp_dir
        # Cleanup is handled by the library's __del__ method

    @pytest.fixture
    def pgp_library(self, temp_gpg_home):
        """Create a PGP library instance with temporary GPG home."""
        return RobotFrameworkPGP(gnupg_home=temp_gpg_home)

    @pytest.fixture
    def test_key_pair(self, pgp_library):
        """Generate a test key pair."""
        fingerprint = pgp_library.generate_key_pair(
            email="test@example.com",
            name="Test User",
            key_length=1024,  # Smaller key for faster testing
            passphrase="testpassword",
        )
        return fingerprint

    def test_library_initialization(self, temp_gpg_home):
        """Test library initialization with custom GPG home."""
        library = RobotFrameworkPGP(gnupg_home=temp_gpg_home)
        assert library._gnupg_home == temp_gpg_home
        assert library._gpg is not None

    def test_library_initialization_default(self):
        """Test library initialization with default GPG home."""
        library = RobotFrameworkPGP()
        assert library._gnupg_home is None
        assert library._temp_dir is not None
        assert library._gpg is not None

    def test_set_gpg_home_directory(self, pgp_library, temp_gpg_home):
        """Test setting GPG home directory."""
        new_temp_dir = tempfile.mkdtemp(prefix="test_gpg_new_")
        pgp_library.set_gpg_home_directory(new_temp_dir)
        assert pgp_library._gnupg_home == new_temp_dir

    def test_generate_key_pair(self, pgp_library):
        """Test key pair generation."""
        fingerprint = pgp_library.generate_key_pair(
            email="test@example.com",
            name="Test User",
            key_length=1024,
            passphrase="testpassword",
        )
        assert fingerprint is not None
        assert len(fingerprint) > 0

    def test_list_keys_empty(self, pgp_library):
        """Test listing keys when keyring is empty."""
        keys = pgp_library.list_keys()
        assert isinstance(keys, list)
        assert len(keys) == 0

    def test_list_keys_with_key(self, pgp_library, test_key_pair):
        """Test listing keys after generating a key pair."""
        keys = pgp_library.list_keys()
        assert len(keys) == 1
        assert keys[0]["fingerprint"] == test_key_pair
        assert "test@example.com" in str(keys[0]["uids"])

    def test_export_public_key(self, pgp_library, test_key_pair):
        """Test exporting public key."""
        public_key = pgp_library.export_public_key("test@example.com")
        assert "BEGIN PGP PUBLIC KEY BLOCK" in public_key
        assert "END PGP PUBLIC KEY BLOCK" in public_key

    def test_export_private_key(self, pgp_library, test_key_pair):
        """Test exporting private key."""
        private_key = pgp_library.export_private_key(
            "test@example.com", passphrase="testpassword"
        )
        assert "BEGIN PGP PRIVATE KEY BLOCK" in private_key
        assert "END PGP PRIVATE KEY BLOCK" in private_key

    def test_encrypt_decrypt_text(self, pgp_library, test_key_pair):
        """Test text encryption and decryption."""
        original_text = "Hello, World! This is a test message."

        # Encrypt
        encrypted_text = pgp_library.encrypt_text(
            text=original_text, recipients="test@example.com"
        )
        assert "BEGIN PGP MESSAGE" in encrypted_text
        assert "END PGP MESSAGE" in encrypted_text

        # Decrypt
        decrypted_text = pgp_library.decrypt_text(
            encrypted_text=encrypted_text, passphrase="testpassword"
        )
        assert decrypted_text == original_text

    def test_encrypt_decrypt_with_multiple_recipients(self, pgp_library):
        """Test encryption with multiple recipients."""
        # Generate two key pairs
        fingerprint1 = pgp_library.generate_key_pair(
            email="user1@example.com",
            name="User One",
            key_length=1024,
            passphrase="password1",
        )
        fingerprint2 = pgp_library.generate_key_pair(
            email="user2@example.com",
            name="User Two",
            key_length=1024,
            passphrase="password2",
        )

        original_text = "Multi-recipient message"
        recipients = ["user1@example.com", "user2@example.com"]

        encrypted_text = pgp_library.encrypt_text(
            text=original_text, recipients=recipients
        )

        # Both users should be able to decrypt
        decrypted1 = pgp_library.decrypt_text(encrypted_text, "password1")
        decrypted2 = pgp_library.decrypt_text(encrypted_text, "password2")

        assert decrypted1 == original_text
        assert decrypted2 == original_text

    def test_encrypt_file(self, pgp_library, test_key_pair, temp_gpg_home):
        """Test file encryption and decryption."""
        # Create test file
        test_content = "This is test file content for encryption."
        input_file = os.path.join(temp_gpg_home, "test_input.txt")
        encrypted_file = os.path.join(temp_gpg_home, "test_encrypted.gpg")
        decrypted_file = os.path.join(temp_gpg_home, "test_decrypted.txt")

        with open(input_file, "w") as f:
            f.write(test_content)

        # Encrypt file
        pgp_library.encrypt_file(
            input_file=input_file,
            output_file=encrypted_file,
            recipients="test@example.com",
        )
        assert os.path.exists(encrypted_file)

        # Decrypt file
        pgp_library.decrypt_file(
            input_file=encrypted_file,
            output_file=decrypted_file,
            passphrase="testpassword",
        )
        assert os.path.exists(decrypted_file)

        # Verify content
        with open(decrypted_file, "r") as f:
            decrypted_content = f.read()
        assert decrypted_content == test_content

    def test_sign_verify_text(self, pgp_library, test_key_pair):
        """Test text signing and verification."""
        original_text = "This text will be signed."

        # Sign text
        signed_text = pgp_library.sign_text(
            text=original_text, key_id="test@example.com", passphrase="testpassword"
        )
        assert "BEGIN PGP SIGNED MESSAGE" in signed_text
        assert original_text in signed_text

        # Verify signature
        verification_result = pgp_library.verify_signature(signed_text)
        assert verification_result["valid"] is True
        assert verification_result["fingerprint"] == test_key_pair

    def test_symmetric_encryption(self, pgp_library):
        """Test symmetric (password-based) encryption."""
        original_text = "Symmetric encryption test message."
        passphrase = "symmetric_password"

        encrypted_text = pgp_library.create_symmetric_encryption(
            text=original_text, passphrase=passphrase
        )
        assert "BEGIN PGP MESSAGE" in encrypted_text

        decrypted_text = pgp_library.decrypt_text(
            encrypted_text=encrypted_text, passphrase=passphrase
        )
        assert decrypted_text == original_text

    def test_import_export_key(self, pgp_library, test_key_pair):
        """Test key import and export functionality."""
        # Export public key
        public_key = pgp_library.export_public_key("test@example.com")

        # Create new library instance (fresh keyring)
        new_library = RobotFrameworkPGP()

        # Import the public key
        fingerprints = new_library.import_key(public_key)
        assert len(fingerprints) == 1
        assert fingerprints[0] == test_key_pair

        # Verify key is available in new instance
        keys = new_library.list_keys()
        assert len(keys) == 1
        assert keys[0]["fingerprint"] == test_key_pair

    def test_get_key_info(self, pgp_library, test_key_pair):
        """Test getting detailed key information."""
        key_info = pgp_library.get_key_info("test@example.com")
        assert key_info["fingerprint"] == test_key_pair
        assert "test@example.com" in str(key_info["uids"])
        assert key_info["length"] == "1024"

    def test_get_gpg_version(self, pgp_library):
        """Test getting GPG version."""
        version = pgp_library.get_gpg_version()
        assert version is not None
        assert len(version) > 0

    #
    # def test_delete_key(self, pgp_library, test_key_pair):
    #     """Test key deletion."""
    #     # Verify key exists
    #     keys = pgp_library.list_keys()
    #     assert len(keys) == 1
    #
    #     # Delete public key (passphrase required for secret key deletion in GnuPG 2.1+)
    #     pgp_library.delete_key("test@example.com", passphrase="testpassword")
    #
    #     # Verify key is deleted
    #     keys = pgp_library.list_keys()
    #     assert len(keys) == 0

    def test_encryption_failure_no_recipient(self, pgp_library):
        """Test encryption failure with non-existent recipient."""
        with pytest.raises(RuntimeError, match="Encryption failed"):
            pgp_library.encrypt_text(
                text="test message", recipients="nonexistent@example.com"
            )

    def test_decryption_failure_wrong_passphrase(self, pgp_library, test_key_pair):
        """Test decryption failure with wrong passphrase."""
        encrypted_text = pgp_library.encrypt_text(
            text="test message", recipients="test@example.com"
        )

        with pytest.raises(RuntimeError, match="Decryption failed"):
            pgp_library.decrypt_text(
                encrypted_text=encrypted_text, passphrase="wrongpassword"
            )

    def test_key_not_found_error(self, pgp_library):
        """Test error when key is not found."""
        with pytest.raises(RuntimeError, match="Key not found"):
            pgp_library.get_key_info("nonexistent@example.com")
