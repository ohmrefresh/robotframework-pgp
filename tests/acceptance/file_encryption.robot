*** Settings ***
Documentation    File encryption and decryption test suite
Library          RobotFrameworkPGP
Library          OperatingSystem
Suite Setup      Initialize File Test Environment
Suite Teardown   Cleanup File Test Environment

*** Variables ***
${TEST_EMAIL}           filetest@example.com
${TEST_NAME}            File Test User
${TEST_PASSPHRASE}      filepassword123
${TEST_FILE_CONTENT}    This is test file content for encryption and decryption testing.
${INPUT_FILE}           ${TEMPDIR}/test_input.txt
${ENCRYPTED_FILE}       ${TEMPDIR}/test_encrypted.gpg
${DECRYPTED_FILE}       ${TEMPDIR}/test_decrypted.txt

*** Test Cases ***
Setup Key For File Testing
    [Documentation]    Generate key pair for file tests
    ${fingerprint}    Generate Key Pair
    ...    email=${TEST_EMAIL}
    ...    name=${TEST_NAME}
    ...    key_length=2048
    ...    passphrase=${TEST_PASSPHRASE}
    Set Suite Variable    ${KEY_FINGERPRINT}    ${fingerprint}

Create Test File
    [Documentation]    Create input file for testing
    Create File    ${INPUT_FILE}    ${TEST_FILE_CONTENT}
    File Should Exist    ${INPUT_FILE}

Encrypt Test File
    [Documentation]    Test file encryption
    Encrypt File
    ...    input_file=${INPUT_FILE}
    ...    output_file=${ENCRYPTED_FILE}
    ...    recipients=${TEST_EMAIL}
    File Should Exist    ${ENCRYPTED_FILE}
    ${encrypted_content}    Get File    ${ENCRYPTED_FILE}
    Should Contain    ${encrypted_content}    BEGIN PGP MESSAGE

Decrypt Test File
    [Documentation]    Test file decryption
    Decrypt File
    ...    input_file=${ENCRYPTED_FILE}
    ...    output_file=${DECRYPTED_FILE}
    ...    passphrase=${TEST_PASSPHRASE}
    File Should Exist    ${DECRYPTED_FILE}

Verify Decrypted Content
    [Documentation]    Verify decrypted file content matches original
    ${decrypted_content}    Get File    ${DECRYPTED_FILE}
    Should Be Equal    ${decrypted_content}    ${TEST_FILE_CONTENT}

*** Keywords ***
Initialize File Test Environment
    [Documentation]    Set up file test environment
    Log    Initializing file encryption test environment
    
Cleanup File Test Environment
    [Documentation]    Clean up file test environment
    Run Keyword And Ignore Error    Remove File    ${INPUT_FILE}
    Run Keyword And Ignore Error    Remove File    ${ENCRYPTED_FILE}
    Run Keyword And Ignore Error    Remove File    ${DECRYPTED_FILE}
    Log    Cleaned up file test environment