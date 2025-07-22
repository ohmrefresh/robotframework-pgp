*** Settings ***
Documentation    Basic encryption and decryption test suite
Library          RobotFrameworkPGP
Suite Setup      Initialize Test Environment
Suite Teardown   Cleanup Test Environment

*** Variables ***
${TEST_EMAIL}           test@example.com
${TEST_NAME}            Test User
${TEST_PASSPHRASE}      testpassword123
${TEST_MESSAGE}         Hello, World! This is a secret message.

*** Test Cases ***
Generate Key Pair
    [Documentation]    Test key pair generation
    ${fingerprint}    Generate Key Pair
    ...    email=${TEST_EMAIL}
    ...    name=${TEST_NAME}
    ...    key_length=2048
    ...    passphrase=${TEST_PASSPHRASE}
    Should Not Be Empty    ${fingerprint}
    Set Suite Variable    ${KEY_FINGERPRINT}    ${fingerprint}

List Keys After Generation
    [Documentation]    Verify key appears in key list
    ${keys}    List Keys
    Length Should Be    ${keys}    1
    Should Contain    ${keys[0]['uids']}    ${TEST_EMAIL}

Export Public Key
    [Documentation]    Test public key export
    ${public_key}    Export Public Key    ${TEST_EMAIL}
    Should Contain    ${public_key}    BEGIN PGP PUBLIC KEY BLOCK
    Should Contain    ${public_key}    END PGP PUBLIC KEY BLOCK
    Set Suite Variable    ${PUBLIC_KEY}    ${public_key}

Encrypt Text Message
    [Documentation]    Test text encryption
    ${encrypted_text}    Encrypt Text
    ...    text=${TEST_MESSAGE}
    ...    recipients=${TEST_EMAIL}
    Should Contain    ${encrypted_text}    BEGIN PGP MESSAGE
    Should Contain    ${encrypted_text}    END PGP MESSAGE
    Set Suite Variable    ${ENCRYPTED_TEXT}    ${encrypted_text}

Decrypt Text Message
    [Documentation]    Test text decryption
    ${decrypted_text}    Decrypt Text
    ...    encrypted_text=${ENCRYPTED_TEXT}
    ...    passphrase=${TEST_PASSPHRASE}
    Should Be Equal    ${decrypted_text}    ${TEST_MESSAGE}

Sign Text Message
    [Documentation]    Test digital signature creation
    ${signed_text}    Sign Text
    ...    text=${TEST_MESSAGE}
    ...    key_id=${TEST_EMAIL}
    ...    passphrase=${TEST_PASSPHRASE}
    Should Contain    ${signed_text}    BEGIN PGP SIGNED MESSAGE
    Should Contain    ${signed_text}    ${TEST_MESSAGE}
    Set Suite Variable    ${SIGNED_TEXT}    ${signed_text}

Verify Text Signature
    [Documentation]    Test signature verification
    ${verification}    Verify Signature    ${SIGNED_TEXT}
    Should Be True    ${verification}[valid]
    Should Be Equal    ${verification}[fingerprint]    ${KEY_FINGERPRINT}

Get Key Information
    [Documentation]    Test retrieving key details
    ${key_info}    Get Key Info    ${TEST_EMAIL}
    Should Be Equal    ${key_info}[fingerprint]    ${KEY_FINGERPRINT}
    Should Contain    ${key_info}[uids]    ${TEST_EMAIL}

*** Keywords ***
Initialize Test Environment
    [Documentation]    Set up test environment
    Log    Initializing PGP test environment
    
Cleanup Test Environment
    [Documentation]    Clean up test environment
    Log    Cleaning up PGP test environment