"""Main Robot Framework PGP Library implementation."""

from robot.api.deco import library

from ._base import _Base
from ._crypto import EncryptionMixin
from ._info import InfoMixin
from ._keys import KeyManagementMixin
from ._signing import SigningMixin


@library(scope="GLOBAL", doc_format="ROBOT")
class RobotFrameworkPGP(
    KeyManagementMixin, EncryptionMixin, SigningMixin, InfoMixin, _Base
):
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
    ROBOT_LIBRARY_VERSION = "1.1.2"
    ROBOT_LIBRARY_DOC_FORMAT = "ROBOT"
