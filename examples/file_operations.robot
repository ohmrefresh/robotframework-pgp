*** Settings ***
Documentation    File encryption and decryption examples
Library          RobotFrameworkPGP
Library          OperatingSystem

*** Variables ***
${TEMP_DIR}    ${TEMPDIR}${/}pgp_examples

*** Test Cases ***
File Encryption Example
    [Documentation]    Demonstrates file encryption and decryption
    [Tags]    example    file
    
    # Setup
    Create Directory    ${TEMP_DIR}
    
    # Generate key pair
    Generate Key Pair    fileuser@example.com    File User    2048    file_secret
    
    # Create a test file
    ${original_file}    Set Variable    ${TEMP_DIR}${/}document.txt
    ${encrypted_file}    Set Variable    ${TEMP_DIR}${/}document.txt.gpg
    ${decrypted_file}    Set Variable    ${TEMP_DIR}${/}document_decrypted.txt
    
    ${file_content}    Set Variable    This is a confidential document.\nIt contains sensitive information.\nPlease keep it secure.
    Create File    ${original_file}    ${file_content}
    
    # Encrypt the file
    Encrypt File
    ...    input_file=${original_file}
    ...    output_file=${encrypted_file}
    ...    recipients=fileuser@example.com
    
    File Should Exist    ${encrypted_file}
    Log    File encrypted successfully
    
    # Decrypt the file
    Decrypt File
    ...    input_file=${encrypted_file}
    ...    output_file=${decrypted_file}
    ...    passphrase=file_secret
    
    File Should Exist    ${decrypted_file}
    
    # Verify content matches
    ${decrypted_content}    Get File    ${decrypted_file}
    Should Be Equal    ${decrypted_content}    ${file_content}
    Log    File decrypted successfully and content verified

Batch File Encryption Example
    [Documentation]    Shows how to encrypt multiple files
    [Tags]    example    batch
    
    # Generate key pair
    Generate Key Pair    batch@example.com    Batch User    2048    batch_secret
    
    # Create multiple test files
    FOR    ${i}    IN RANGE    1    4
        ${file_path}    Set Variable    ${TEMP_DIR}${/}file${i}.txt
        ${content}    Set Variable    Content of file number ${i}
        Create File    ${file_path}    ${content}
        
        ${encrypted_path}    Set Variable    ${TEMP_DIR}${/}file${i}.txt.gpg
        Encrypt File
        ...    input_file=${file_path}
        ...    output_file=${encrypted_path}
        ...    recipients=batch@example.com
        
        File Should Exist    ${encrypted_path}
        Log    Encrypted file${i}.txt
    END
    
    Log    All files encrypted successfully

Key Management Example
    [Documentation]    Demonstrates key import/export operations
    [Tags]    example    keys
    
    # Generate a key pair
    Generate Key Pair    keyuser@example.com    Key User    2048    key_secret
    
    # Export public key to file
    ${public_key}    Export Public Key    keyuser@example.com
    ${public_key_file}    Set Variable    ${TEMP_DIR}${/}public_key.asc
    Create File    ${public_key_file}    ${public_key}
    
    # List current keys
    ${keys_before}    List Keys
    ${count_before}    Get Length    ${keys_before}
    
    # Delete the key
    Delete Key    keyuser@example.com
    
    # Verify key is deleted
    ${keys_after_delete}    List Keys
    ${count_after_delete}    Get Length    ${keys_after_delete}
    Should Be Equal As Numbers    ${count_after_delete}    ${count_before - 1}
    
    # Re-import from file
    Import Key From File    ${public_key_file}
    
    # Verify key is back
    ${keys_after_import}    List Keys
    ${count_after_import}    Get Length    ${keys_after_import}
    Should Be Equal As Numbers    ${count_after_import}    ${count_before}
    
    Log    Key export/import cycle completed successfully

*** Keywords ***
Suite Teardown
    [Documentation]    Clean up example files
    Run Keyword And Ignore Error    Remove Directory    ${TEMP_DIR}    recursive=True