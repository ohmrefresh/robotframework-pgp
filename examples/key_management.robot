*** Settings ***
Documentation    Key management and utility keyword examples
Library          RobotFrameworkPGP
Library          OperatingSystem
Suite Setup      Setup Isolated GPG Home
Suite Teardown   Cleanup Example Files

*** Variables ***
${WORK_DIR}     ${TEMPDIR}${/}pgp_key_examples
${GPG_HOME}     ${WORK_DIR}${/}gnupg

*** Test Cases ***
GPG Version Example
    [Documentation]    Shows how to inspect the GPG installation
    [Tags]    example    utility

    ${version}    Get GPG Version
    Should Not Be Empty    ${version}
    Log    Using GPG version: ${version}

Key Info Example
    [Documentation]    Demonstrates inspecting a key's details
    [Tags]    example    keys

    ${fingerprint}    Generate Key Pair
    ...    email=inspector@example.com
    ...    name=Inspector Gadget
    ...    key_length=2048
    ...    passphrase=inspect_secret

    ${info}    Get Key Info    inspector@example.com
    Should Be Equal    ${info}[fingerprint]    ${fingerprint}
    Should Not Be Empty    ${info}[keyid]
    Log    Key ID: ${info}[keyid], created: ${info}[date]

Export And Import Private Key Example
    [Documentation]    Round-trips a private key through export and re-import.
    ...    WARNING: exported private keys are secrets — never log them or
    ...    commit them to version control. This example only writes to a
    ...    throwaway temp directory that is removed in the suite teardown.
    [Tags]    example    keys

    Generate Key Pair    backup@example.com    Backup User    2048    backup_secret

    # Export both halves of the key pair
    ${public_key}    Export Public Key    backup@example.com
    Should Contain    ${public_key}    BEGIN PGP PUBLIC KEY BLOCK
    ${private_key}    Export Private Key    backup@example.com    backup_secret
    Should Contain    ${private_key}    BEGIN PGP PRIVATE KEY BLOCK

    # Save the private key to a file (temp dir only!)
    ${private_key_file}    Set Variable    ${WORK_DIR}${/}backup_private.asc
    Create File    ${private_key_file}    ${private_key}

    # Delete the key, then restore it from the exported file
    Delete Key    backup@example.com    secret=${True}    passphrase=backup_secret
    ${fingerprints}    Import Key From File    ${private_key_file}
    Should Not Be Empty    ${fingerprints}

    # The restored key can decrypt again
    ${encrypted}    Encrypt Text    Restored and working    backup@example.com
    ${decrypted}    Decrypt Text    ${encrypted}    passphrase=backup_secret
    Should Be Equal    ${decrypted}    Restored and working

*** Keywords ***
Setup Isolated GPG Home
    [Documentation]    Point the library at a throwaway GPG home directory
    ...    so this suite never touches the user's real keyring.
    Create Directory    ${GPG_HOME}
    Set GPG Home Directory    ${GPG_HOME}

Cleanup Example Files
    Run Keyword And Ignore Error    Remove Directory    ${WORK_DIR}    recursive=True
