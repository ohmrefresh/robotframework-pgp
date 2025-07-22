Keyword Reference
=================

This page provides detailed documentation for all keywords available in the Robot Framework PGP library.

Configuration Keywords
-----------------------

Set GPG Home Directory
~~~~~~~~~~~~~~~~~~~~~~~

Sets the GPG home directory path.

**Arguments:**
- ``gnupg_home`` (str): Path to the GPG home directory

**Example:**

.. code-block:: robotframework

   Set GPG Home Directory    /path/to/gnupg

Key Management Keywords
-----------------------

Generate Key Pair
~~~~~~~~~~~~~~~~~~

Generates a new GPG key pair.

**Arguments:**
- ``email`` (str): Email address for the key
- ``name`` (str): Name for the key
- ``key_length`` (int, optional): Key length in bits (default: 2048)
- ``passphrase`` (str, optional): Passphrase to protect the private key
- ``expire_date`` (str, optional): Expiration date (default: "0" for no expiration)

**Returns:**
- Key fingerprint (str)

**Example:**

.. code-block:: robotframework

   ${fingerprint}    Generate Key Pair
   ...    email=alice@example.com
   ...    name=Alice Smith
   ...    key_length=4096
   ...    passphrase=secret123

Import Key
~~~~~~~~~~

Imports a GPG key from key data.

**Arguments:**
- ``key_data`` (str): The key data to import (ASCII armored)

**Returns:**
- List of imported key fingerprints

**Example:**

.. code-block:: robotframework

   ${fingerprints}    Import Key    ${public_key_data}

Import Key From File
~~~~~~~~~~~~~~~~~~~~

Imports a GPG key from a file.

**Arguments:**
- ``key_file_path`` (str): Path to the key file

**Returns:**
- List of imported key fingerprints

**Example:**

.. code-block:: robotframework

   ${fingerprints}    Import Key From File    /path/to/key.asc

Export Public Key
~~~~~~~~~~~~~~~~~

Exports a public key.

**Arguments:**
- ``key_id`` (str): Key ID, fingerprint, or email address

**Returns:**
- ASCII armored public key (str)

**Example:**

.. code-block:: robotframework

   ${public_key}    Export Public Key    alice@example.com

Export Private Key
~~~~~~~~~~~~~~~~~~

Exports a private key.

**Arguments:**
- ``key_id`` (str): Key ID, fingerprint, or email address
- ``passphrase`` (str, optional): Passphrase to unlock the private key

**Returns:**
- ASCII armored private key (str)

**Example:**

.. code-block:: robotframework

   ${private_key}    Export Private Key
   ...    key_id=alice@example.com
   ...    passphrase=secret123

List Keys
~~~~~~~~~

Lists GPG keys.

**Arguments:**
- ``secret`` (bool, optional): If True, list secret keys; otherwise list public keys (default: False)

**Returns:**
- List of key information dictionaries

**Example:**

.. code-block:: robotframework

   ${public_keys}    List Keys
   ${secret_keys}    List Keys    secret=${True}

Get Key Info
~~~~~~~~~~~~

Gets detailed information about a specific key.

**Arguments:**
- ``key_id`` (str): Key ID, fingerprint, or email address

**Returns:**
- Dictionary with key information

**Example:**

.. code-block:: robotframework

   ${key_info}    Get Key Info    alice@example.com
   Log    Key fingerprint: ${key_info}[fingerprint]

Delete Key
~~~~~~~~~~

Deletes a GPG key.

**Arguments:**
- ``key_id`` (str): Key ID, fingerprint, or email address
- ``secret`` (bool, optional): If True, delete secret key; otherwise delete public key (default: False)
- ``passphrase`` (str, optional): Passphrase to unlock the private key (for secret key deletion)

**Example:**

.. code-block:: robotframework

   Delete Key    alice@example.com
   Delete Key    alice@example.com    secret=${True}    passphrase=secret123

Encryption/Decryption Keywords
------------------------------

Encrypt Text
~~~~~~~~~~~~

Encrypts text for specified recipients.

**Arguments:**
- ``text`` (str): Text to encrypt
- ``recipients`` (str or list): Recipient key ID(s), fingerprint(s), or email address(es)
- ``sign`` (str, optional): Optional key ID to sign with
- ``passphrase`` (str, optional): Passphrase for signing key
- ``armor`` (bool, optional): If True, return ASCII armored output (default: True)

**Returns:**
- Encrypted text (str)

**Example:**

.. code-block:: robotframework

   ${encrypted}    Encrypt Text
   ...    text=Secret message
   ...    recipients=alice@example.com
   
   ${signed_encrypted}    Encrypt Text
   ...    text=Authenticated message
   ...    recipients=alice@example.com
   ...    sign=bob@example.com
   ...    passphrase=bob_secret

Decrypt Text
~~~~~~~~~~~~

Decrypts encrypted text.

**Arguments:**
- ``encrypted_text`` (str): Encrypted text to decrypt
- ``passphrase`` (str, optional): Passphrase to unlock the private key

**Returns:**
- Decrypted text (str)

**Example:**

.. code-block:: robotframework

   ${decrypted}    Decrypt Text
   ...    encrypted_text=${encrypted_message}
   ...    passphrase=secret123

Encrypt File
~~~~~~~~~~~~

Encrypts a file for specified recipients.

**Arguments:**
- ``input_file`` (str): Path to the input file
- ``output_file`` (str): Path to the output encrypted file
- ``recipients`` (str or list): Recipient key ID(s), fingerprint(s), or email address(es)
- ``sign`` (str, optional): Optional key ID to sign with
- ``passphrase`` (str, optional): Passphrase for signing key
- ``armor`` (bool, optional): If True, create ASCII armored output (default: True)

**Example:**

.. code-block:: robotframework

   Encrypt File
   ...    input_file=document.txt
   ...    output_file=document.txt.gpg
   ...    recipients=alice@example.com

Decrypt File
~~~~~~~~~~~~

Decrypts an encrypted file.

**Arguments:**
- ``input_file`` (str): Path to the encrypted input file
- ``output_file`` (str): Path to the decrypted output file
- ``passphrase`` (str, optional): Passphrase to unlock the private key

**Example:**

.. code-block:: robotframework

   Decrypt File
   ...    input_file=document.txt.gpg
   ...    output_file=document.txt
   ...    passphrase=secret123

Create Symmetric Encryption
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creates symmetric encryption (password-based).

**Arguments:**
- ``text`` (str): Text to encrypt
- ``passphrase`` (str): Passphrase for encryption

**Returns:**
- Encrypted text (str)

**Example:**

.. code-block:: robotframework

   ${encrypted}    Create Symmetric Encryption
   ...    text=Secret data
   ...    passphrase=shared_password

Digital Signature Keywords
---------------------------

Sign Text
~~~~~~~~~

Creates a digital signature for text.

**Arguments:**
- ``text`` (str): Text to sign
- ``key_id`` (str): Key ID, fingerprint, or email address to sign with
- ``passphrase`` (str, optional): Passphrase to unlock the private key

**Returns:**
- Signed text (str) - cleartext signature

**Example:**

.. code-block:: robotframework

   ${signed_text}    Sign Text
   ...    text=Important document
   ...    key_id=alice@example.com
   ...    passphrase=secret123

Verify Signature
~~~~~~~~~~~~~~~~

Verifies a digital signature.

**Arguments:**
- ``signed_text`` (str): Signed text to verify

**Returns:**
- Dictionary with verification results

**Example:**

.. code-block:: robotframework

   ${result}    Verify Signature    ${signed_text}
   Should Be True    ${result}[valid]
   Log    Signed by: ${result}[username]

Utility Keywords
----------------

Get GPG Version
~~~~~~~~~~~~~~~

Gets the GPG version information.

**Returns:**
- GPG version string (str)

**Example:**

.. code-block:: robotframework

   ${version}    Get GPG Version
   Log    Using GPG version: ${version}

Return Value Details
--------------------

Key Information Dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``List Keys`` and ``Get Key Info`` keywords return dictionaries with the following structure:

.. code-block:: python

   {
       'fingerprint': 'ABC123...',      # Key fingerprint
       'keyid': '12345678',             # Short key ID
       'uids': ['Name <email>'],        # User IDs
       'length': '2048',                # Key length
       'algo': '1',                     # Algorithm
       'expires': '',                   # Expiration date
       'trust': 'u',                    # Trust level
       'date': '2024-01-01',           # Creation date
       'subkeys': [...]                 # Subkey information
   }

Verification Result Dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``Verify Signature`` keyword returns a dictionary with:

.. code-block:: python

   {
       'valid': True,                   # Signature validity
       'fingerprint': 'ABC123...',      # Signer's fingerprint
       'key_id': '12345678',           # Signer's key ID
       'username': 'Name <email>',      # Signer's name/email
       'trust_level': 'TRUST_ULTIMATE', # Trust level
       'trust_text': 'ultimate',        # Trust text
       'signature_id': 'SIG123...',     # Signature ID
       'timestamp': 1234567890          # Signature timestamp
   }