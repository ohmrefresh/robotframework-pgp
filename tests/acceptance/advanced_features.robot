*** Settings ***
Documentation    Advanced PGP features test suite
Library          RobotFrameworkPGP
Suite Setup      Initialize Advanced Test Environment
Suite Teardown   Cleanup Advanced Test Environment

*** Variables ***
${USER1_EMAIL}          user1@example.com
${USER1_NAME}           User One
${USER1_PASSPHRASE}     password1
${USER2_EMAIL}          user2@example.com
${USER2_NAME}           User Two
${USER2_PASSPHRASE}     password2
${SYMMETRIC_MESSAGE}    Symmetric encryption test message
${SYMMETRIC_PASSWORD}   symmetric123
${MULTI_USER_MESSAGE}   This message is for multiple recipients

*** Test Cases ***
Generate Multiple Key Pairs
    [Documentation]    Generate key pairs for multiple users
    ${fingerprint1}    Generate Key Pair
    ...    email=${USER1_EMAIL}
    ...    name=${USER1_NAME}
    ...    key_length=2048
    ...    passphrase=${USER1_PASSPHRASE}
    Set Suite Variable    ${USER1_FINGERPRINT}    ${fingerprint1}
    
    ${fingerprint2}    Generate Key Pair
    ...    email=${USER2_EMAIL}
    ...    name=${USER2_NAME}
    ...    key_length=2048
    ...    passphrase=${USER2_PASSPHRASE}
    Set Suite Variable    ${USER2_FINGERPRINT}    ${fingerprint2}

Test Multiple Recipients Encryption
    [Documentation]    Test encryption for multiple recipients
    @{recipients}    Create List    ${USER1_EMAIL}    ${USER2_EMAIL}
    ${encrypted_text}    Encrypt Text
    ...    text=${MULTI_USER_MESSAGE}
    ...    recipients=${recipients}
    Set Suite Variable    ${MULTI_ENCRYPTED_TEXT}    ${encrypted_text}

Test Multiple Recipients Decryption By User1
    [Documentation]    Verify first user can decrypt multi-recipient message
    ${decrypted_text}    Decrypt Text
    ...    encrypted_text=${MULTI_ENCRYPTED_TEXT}
    ...    passphrase=${USER1_PASSPHRASE}
    Should Be Equal    ${decrypted_text}    ${MULTI_USER_MESSAGE}

Test Multiple Recipients Decryption By User2
    [Documentation]    Verify second user can decrypt multi-recipient message
    ${decrypted_text}    Decrypt Text
    ...    encrypted_text=${MULTI_ENCRYPTED_TEXT}
    ...    passphrase=${USER2_PASSPHRASE}
    Should Be Equal    ${decrypted_text}    ${MULTI_USER_MESSAGE}

Test Symmetric Encryption
    [Documentation]    Test password-based symmetric encryption
    ${symmetric_encrypted}    Create Symmetric Encryption
    ...    text=${SYMMETRIC_MESSAGE}
    ...    passphrase=${SYMMETRIC_PASSWORD}
    Should Contain    ${symmetric_encrypted}    BEGIN PGP MESSAGE
    
    ${symmetric_decrypted}    Decrypt Text
    ...    encrypted_text=${symmetric_encrypted}
    ...    passphrase=${SYMMETRIC_PASSWORD}
    Should Be Equal    ${symmetric_decrypted}    ${SYMMETRIC_MESSAGE}

Test Sign And Encrypt
    [Documentation]    Test signing and encrypting in one operation
    ${signed_encrypted}    Encrypt Text
    ...    text=${MULTI_USER_MESSAGE}
    ...    recipients=${USER1_EMAIL}
    ...    sign=${USER2_EMAIL}
    ...    passphrase=${USER2_PASSPHRASE}
    
    ${decrypted_signed}    Decrypt Text
    ...    encrypted_text=${signed_encrypted}
    ...    passphrase=${USER1_PASSPHRASE}
    Should Be Equal    ${decrypted_signed}    ${MULTI_USER_MESSAGE}

Test GPG Version Information
    [Documentation]    Test getting GPG version
    ${version}    Get GPG Version
    Should Not Be Empty    ${version}
    Log    GPG Version: ${version}

*** Keywords ***
Initialize Advanced Test Environment
    [Documentation]    Set up advanced test environment
    Log    Initializing advanced PGP test environment
    
Cleanup Advanced Test Environment
    [Documentation]    Clean up advanced test environment
    Log    Cleaning up advanced PGP test environment