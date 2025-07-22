Robot Framework PGP Library
===========================

A Robot Framework library for PGP/GPG encryption and decryption operations.

Features
--------

- **Text Encryption/Decryption**: Encrypt and decrypt text messages
- **File Encryption/Decryption**: Secure file operations
- **Digital Signatures**: Create and verify digital signatures
- **Key Management**: Generate, import, export, and manage GPG keys
- **Multiple Recipients**: Encrypt messages for multiple recipients
- **Symmetric Encryption**: Password-based encryption without keys

Installation
------------

.. code-block:: bash

   pip install robotframework-pgp

Quick Start
-----------

.. code-block:: robotframework

   *** Settings ***
   Library    RobotFrameworkPGP

   *** Test Cases ***
   Basic Encryption Example
       # Generate a key pair
       ${fingerprint}    Generate Key Pair
       ...    email=alice@example.com
       ...    name=Alice Smith
       ...    passphrase=secret123
       
       # Encrypt a message
       ${encrypted}    Encrypt Text
       ...    text=Hello, World!
       ...    recipients=alice@example.com
       
       # Decrypt the message
       ${decrypted}    Decrypt Text
       ...    encrypted_text=${encrypted}
       ...    passphrase=secret123
       
       Should Be Equal    ${decrypted}    Hello, World!

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide:

   installation
   quickstart
   examples
   keywords

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api

.. toctree::
   :maxdepth: 1
   :caption: Development:

   contributing
   changelog

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`