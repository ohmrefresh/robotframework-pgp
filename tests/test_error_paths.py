"""Mock-based tests for error paths that cannot be triggered with a real GPG binary."""

from unittest import mock

import pytest

from RobotFrameworkPGP import RobotFrameworkPGP


@pytest.fixture
def mock_library(tmp_path):
    """Library instance whose GPG backend is a MagicMock (no gpg binary used)."""
    with mock.patch("RobotFrameworkPGP._base.gnupg.GPG") as gpg_cls:
        library = RobotFrameworkPGP(gnupg_home=str(tmp_path / "gpg"))
        yield library, gpg_cls.return_value


class TestKeyManagementErrorPaths:
    """Error branches in key management keywords."""

    def test_generate_key_pair_failure(self, mock_library):
        library, gpg = mock_library
        gpg.gen_key.return_value = None
        with pytest.raises(RuntimeError, match="Failed to generate key pair"):
            library.generate_key_pair(email="a@b.com", name="A B")

    def test_import_key_no_keys_imported(self, mock_library):
        library, gpg = mock_library
        gpg.import_keys.return_value = mock.Mock(count=0)
        with pytest.raises(RuntimeError, match="Failed to import any keys"):
            library.import_key("garbage")

    def test_delete_secret_key_failure(self, mock_library):
        library, gpg = mock_library
        key = {"fingerprint": "ABC", "keyid": "ABC", "uids": ["A <a@b.com>"]}
        gpg.list_keys.return_value = [key]
        gpg.delete_keys.return_value = mock.Mock(status="failure", stderr="boom")
        with pytest.raises(RuntimeError, match="Secret key deletion failed"):
            library.delete_key("ABC", secret=True, passphrase="pw")

    def test_delete_public_key_failure(self, mock_library):
        library, gpg = mock_library
        key = {"fingerprint": "ABC", "keyid": "ABC", "uids": ["A <a@b.com>"]}
        gpg.list_keys.return_value = [key]
        gpg.delete_keys.return_value = mock.Mock(status="failure", stderr="boom")
        with pytest.raises(RuntimeError, match="Key deletion failed"):
            library.delete_key("ABC")

    def test_delete_public_key_without_secret_key(self, mock_library):
        library, gpg = mock_library
        key = {"fingerprint": "ABC", "keyid": "ABC", "uids": ["A <a@b.com>"]}
        calls = {"n": 0}

        def list_keys(secret=False):
            if secret:
                return []
            # Key exists before deletion, gone afterwards.
            calls["n"] += 1
            return [key] if calls["n"] == 1 else []

        gpg.list_keys.side_effect = list_keys
        gpg.delete_keys.return_value = mock.Mock(status="ok")
        library.delete_key("ABC")
        gpg.delete_keys.assert_called_once_with("ABC", secret=False)


class TestSigningErrorPaths:
    """Error branches in signing keywords."""

    def test_sign_text_failure(self, mock_library):
        library, gpg = mock_library
        gpg.sign.return_value = ""
        with pytest.raises(RuntimeError, match="Text signing failed"):
            library.sign_text("hello", key_id="ABC")


class TestGetGpgVersion:
    """All branches of Get GPG Version."""

    def test_version_attribute(self, mock_library):
        library, gpg = mock_library
        gpg.version = "2.4.0"
        assert library.get_gpg_version() == "2.4.0"

    def test_binary_version_attribute(self, mock_library):
        library, gpg = mock_library
        del gpg.version
        gpg.binary_version = "2.4.1"
        assert library.get_gpg_version() == "2.4.1"

    def test_subprocess_fallback_success(self, mock_library):
        library, gpg = mock_library
        del gpg.version
        del gpg.binary_version
        completed = mock.Mock(returncode=0, stdout="gpg (GnuPG) 2.4.3\nother")
        with mock.patch("subprocess.run", return_value=completed):
            assert library.get_gpg_version() == "gpg (GnuPG) 2.4.3"

    def test_subprocess_fallback_nonzero_exit(self, mock_library):
        library, gpg = mock_library
        del gpg.version
        del gpg.binary_version
        completed = mock.Mock(returncode=1, stdout="")
        with mock.patch("subprocess.run", return_value=completed):
            assert library.get_gpg_version() == "Unknown"

    def test_subprocess_fallback_exception(self, mock_library):
        library, gpg = mock_library
        del gpg.version
        del gpg.binary_version
        with mock.patch("subprocess.run", side_effect=OSError("no gpg")):
            assert library.get_gpg_version() == "Unknown"
