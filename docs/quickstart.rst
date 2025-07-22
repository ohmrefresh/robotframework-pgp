Quick Start Guide
=================

This guide will help you get started with the Robot Framework PGP library.

Basic Concepts
--------------

**Public Key Cryptography**
   Uses a pair of keys (public and private) where the public key encrypts and the private key decrypts.

**Symmetric Cryptography**
   Uses a single password/passphrase for both encryption and decryption.

**Digital Signatures**
   Uses your private key to sign a message, allowing others to verify it came from you using your public key.

First Steps
-----------

1. **Import the Library**

.. code-block:: robotframework

   *** Settings ***
   Library    RobotFrameworkPGP

2. **Generate a Key Pair**

.. code-block:: robotframework

   *** Test Cases ***
   Setup Keys
       ${fingerprint}    Generate Key Pair
       ...    email=user@example.com
       ...    name=Test User
       ...    key_length=2048
       ...    passphrase=mypassword

3. **Encrypt and Decrypt Text**

.. code-block:: robotframework

   *** Test Cases ***
   Basic Encryption
       ${encrypted}    Encrypt Text
       ...    text=Hello, World!
       ...    recipients=user@example.com
       
       ${decrypted}    Decrypt Text
       ...    encrypted_text=${encrypted}
       ...    passphrase=mypassword

Complete Example
----------------

Here's a complete Robot Framework test file:

.. code-block:: robotframework

   *** Settings ***
   Library    RobotFrameworkPGP

   *** Variables ***
   ${EMAIL}       alice@example.com
   ${NAME}        Alice Smith
   ${PASSPHRASE}  secret123
   ${MESSAGE}     This is a confidential message!

   *** Test Cases ***
   Complete PGP Workflow
       [Documentation]    Demonstrates key generation, encryption, and decryption
       
       # Step 1: Generate key pair
       ${fingerprint}    Generate Key Pair
       ...    email=${EMAIL}
       ...    name=${NAME}
       ...    key_length=2048
       ...    passphrase=${PASSPHRASE}
       
       # Step 2: Encrypt message
       ${encrypted_message}    Encrypt Text
       ...    text=${MESSAGE}
       ...    recipients=${EMAIL}
       
       # Step 3: Decrypt message
       ${decrypted_message}    Decrypt Text
       ...    encrypted_text=${encrypted_message}
       ...    passphrase=${PASSPHRASE}
       
       # Step 4: Verify message
       Should Be Equal    ${decrypted_message}    ${MESSAGE}
       Log    Success! Message encrypted and decrypted correctly.

Common Use Cases
----------------

**Multiple Recipients**

.. code-block:: robotframework

   @{recipients}    Create List    alice@example.com    bob@example.com
   ${encrypted}    Encrypt Text    ${message}    ${recipients}

**File Encryption**

.. code-block:: robotframework

   Encrypt File
   ...    input_file=document.txt
   ...    output_file=document.txt.gpg
   ...    recipients=alice@example.com

**Digital Signatures**

.. code-block:: robotframework

   ${signed}    Sign Text
   ...    text=${document}
   ...    key_id=alice@example.com
   ...    passphrase=secret123
   
   ${verification}    Verify Signature    ${signed}
   Should Be True    ${verification}[valid]

**Symmetric Encryption**

.. code-block:: robotframework

   ${encrypted}    Create Symmetric Encryption
   ...    text=${message}
   ...    passphrase=shared_secret
   
   ${decrypted}    Decrypt Text
   ...    encrypted_text=${encrypted}
   ...    passphrase=shared_secret

Best Practices
--------------

1. **Use Strong Passphrases**: Always use strong, unique passphrases for your keys.

2. **Key Length**: Use at least 2048-bit keys for security (4096-bit for high security).

3. **Test Environment**: Use separate GPG directories for testing to avoid interfering with your personal keys.

4. **Cleanup**: The library automatically cleans up temporary directories, but you can also manage this manually.

5. **Error Handling**: Always handle potential errors in your test cases:

.. code-block:: robotframework

   ${status}    Run Keyword And Return Status    Decrypt Text    ${encrypted}    wrongpassword
   Should Be Equal    ${status}    ${False}

Next Steps
----------

- Explore the :doc:`examples` for more complex scenarios
- Check the :doc:`keywords` reference for all available keywords
- See the :doc:`api` documentation for detailed parameter information