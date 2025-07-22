Examples
========

This page provides comprehensive examples of using the Robot Framework PGP library.

Basic Text Encryption
----------------------

Simple encryption and decryption of text messages:

.. code-block:: robotframework

   *** Settings ***
   Library    RobotFrameworkPGP

   *** Test Cases ***
   Simple Text Encryption
       # Generate key pair
       Generate Key Pair    alice@example.com    Alice Smith    2048    alice_secret
       
       # Encrypt text
       ${encrypted}    Encrypt Text
       ...    text=Confidential information
       ...    recipients=alice@example.com
       
       # Decrypt text
       ${decrypted}    Decrypt Text
       ...    encrypted_text=${encrypted}
       ...    passphrase=alice_secret
       
       Should Be Equal    ${decrypted}    Confidential information

File Encryption
---------------

Encrypting and decrypting files:

.. code-block:: robotframework

   *** Settings ***
   Library    RobotFrameworkPGP
   Library    OperatingSystem

   *** Test Cases ***
   File Encryption Example
       # Setup
       Generate Key Pair    user@example.com    File User    2048    file_secret
       
       # Create test file
       Create File    input.txt    This is sensitive file content.
       
       # Encrypt file
       Encrypt File
       ...    input_file=input.txt
       ...    output_file=input.txt.gpg
       ...    recipients=user@example.com
       
       # Decrypt file
       Decrypt File
       ...    input_file=input.txt.gpg
       ...    output_file=output.txt
       ...    passphrase=file_secret
       
       # Verify content
       ${content}    Get File    output.txt
       Should Contain    ${content}    sensitive file content

Multiple Recipients
-------------------

Encrypting messages for multiple recipients:

.. code-block:: robotframework

   *** Test Cases ***
   Multiple Recipients Encryption
       # Generate multiple key pairs
       Generate Key Pair    alice@example.com    Alice    2048    alice_pass
       Generate Key Pair    bob@example.com      Bob      2048    bob_pass
       Generate Key Pair    carol@example.com    Carol    2048    carol_pass
       
       # Create recipient list
       @{recipients}    Create List
       ...    alice@example.com
       ...    bob@example.com
       ...    carol@example.com
       
       # Encrypt for all recipients
       ${encrypted}    Encrypt Text
       ...    text=Team meeting at 2 PM
       ...    recipients=${recipients}
       
       # Each recipient can decrypt
       ${alice_msg}    Decrypt Text    ${encrypted}    alice_pass
       ${bob_msg}      Decrypt Text    ${encrypted}    bob_pass
       ${carol_msg}    Decrypt Text    ${encrypted}    carol_pass
       
       # All should have the same message
       Should Be Equal    ${alice_msg}    Team meeting at 2 PM
       Should Be Equal    ${bob_msg}      Team meeting at 2 PM
       Should Be Equal    ${carol_msg}    Team meeting at 2 PM

Digital Signatures
------------------

Creating and verifying digital signatures:

.. code-block:: robotframework

   *** Test Cases ***
   Digital Signature Example
       # Generate key pair for signing
       ${fingerprint}    Generate Key Pair
       ...    email=signer@example.com
       ...    name=Document Signer
       ...    passphrase=sign_secret
       
       # Sign a document
       ${document}    Set Variable    Contract: Payment of $10,000 due by 2024-12-31
       ${signed}    Sign Text
       ...    text=${document}
       ...    key_id=signer@example.com
       ...    passphrase=sign_secret
       
       # Verify signature
       ${verification}    Verify Signature    ${signed}
       Should Be True         ${verification}[valid]
       Should Be Equal        ${verification}[fingerprint]    ${fingerprint}
       Should Contain         ${verification}[username]       signer@example.com
       
       Log    Document successfully signed and verified

Sign and Encrypt
----------------

Combining signatures with encryption:

.. code-block:: robotframework

   *** Test Cases ***
   Sign And Encrypt Example
       # Generate keys
       Generate Key Pair    sender@example.com     Sender    2048    sender_pass
       Generate Key Pair    recipient@example.com  Recipient 2048    recipient_pass
       
       # Sign and encrypt in one operation
       ${message}    Set Variable    Authenticated and encrypted message
       ${signed_encrypted}    Encrypt Text
       ...    text=${message}
       ...    recipients=recipient@example.com
       ...    sign=sender@example.com
       ...    passphrase=sender_pass
       
       # Decrypt (signature verification is automatic)
       ${decrypted}    Decrypt Text
       ...    encrypted_text=${signed_encrypted}
       ...    passphrase=recipient_pass
       
       Should Be Equal    ${decrypted}    ${message}

Symmetric Encryption
--------------------

Password-based encryption without keys:

.. code-block:: robotframework

   *** Test Cases ***
   Symmetric Encryption Example
       ${secret_data}    Set Variable    Password: admin123, PIN: 4567
       ${password}       Set Variable    vault_master_key_2024
       
       # Encrypt with password
       ${encrypted}    Create Symmetric Encryption
       ...    text=${secret_data}
       ...    passphrase=${password}
       
       # Decrypt with same password
       ${decrypted}    Decrypt Text
       ...    encrypted_text=${encrypted}
       ...    passphrase=${password}
       
       Should Be Equal    ${decrypted}    ${secret_data}

Key Management
--------------

Managing GPG keys:

.. code-block:: robotframework

   *** Test Cases ***
   Key Management Example
       # Generate key
       ${fp1}    Generate Key Pair    test1@example.com    User1    2048    pass1
       ${fp2}    Generate Key Pair    test2@example.com    User2    2048    pass2
       
       # List all keys
       ${all_keys}    List Keys
       Length Should Be    ${all_keys}    2
       
       # Get specific key info
       ${key_info}    Get Key Info    test1@example.com
       Should Be Equal    ${key_info}[fingerprint]    ${fp1}
       
       # Export public key
       ${public_key}    Export Public Key    test1@example.com
       Should Contain    ${public_key}    BEGIN PGP PUBLIC KEY BLOCK
       
       # Delete and re-import key
       Delete Key    test1@example.com
       ${keys_after_delete}    List Keys
       Length Should Be    ${keys_after_delete}    1
       
       Import Key    ${public_key}
       ${keys_after_import}    List Keys
       Length Should Be    ${keys_after_import}    2

Batch Operations
----------------

Processing multiple files or messages:

.. code-block:: robotframework

   *** Settings ***
   Library    RobotFrameworkPGP
   Library    OperatingSystem

   *** Test Cases ***
   Batch File Processing
       # Setup
       Generate Key Pair    batch@example.com    Batch User    2048    batch_pass
       Create Directory    input_files
       Create Directory    encrypted_files
       Create Directory    decrypted_files
       
       # Create multiple input files
       FOR    ${i}    IN RANGE    1    6
           Create File    input_files/file${i}.txt    Content of file ${i}
       END
       
       # Encrypt all files
       @{input_files}    List Files In Directory    input_files
       FOR    ${file}    IN    @{input_files}
           ${input_path}    Set Variable    input_files/${file}
           ${encrypted_path}    Set Variable    encrypted_files/${file}.gpg
           
           Encrypt File
           ...    input_file=${input_path}
           ...    output_file=${encrypted_path}
           ...    recipients=batch@example.com
       END
       
       # Decrypt all files
       @{encrypted_files}    List Files In Directory    encrypted_files
       FOR    ${file}    IN    @{encrypted_files}
           ${encrypted_path}    Set Variable    encrypted_files/${file}
           ${decrypted_path}    Set Variable    decrypted_files/${file}
           
           Decrypt File
           ...    input_file=${encrypted_path}
           ...    output_file=${decrypted_path}
           ...    passphrase=batch_pass
       END

Error Handling
--------------

Proper error handling in tests:

.. code-block:: robotframework

   *** Test Cases ***
   Error Handling Example
       Generate Key Pair    test@example.com    Test User    2048    secret
       
       # Test wrong recipient
       ${status}    Run Keyword And Return Status
       ...    Encrypt Text    message    nonexistent@example.com
       Should Be Equal    ${status}    ${False}
       
       # Test wrong passphrase
       ${encrypted}    Encrypt Text    message    test@example.com
       ${status}    Run Keyword And Return Status
       ...    Decrypt Text    ${encrypted}    wrong_passphrase
       Should Be Equal    ${status}    ${False}
       
       # Test missing key
       ${status}    Run Keyword And Return Status
       ...    Get Key Info    missing@example.com
       Should Be Equal    ${status}    ${False}

Configuration Examples
----------------------

Custom GPG home directory:

.. code-block:: robotframework

   *** Settings ***
   Library    RobotFrameworkPGP    gnupg_home=/tmp/my_test_gpg

   *** Test Cases ***
   Custom GPG Directory
       # Library is already using /tmp/my_test_gpg
       ${version}    Get GPG Version
       Log    Using GPG version: ${version}
       
       # Or change it dynamically
       Set GPG Home Directory    /tmp/another_gpg_dir