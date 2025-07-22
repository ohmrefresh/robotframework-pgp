*** Settings ***
Documentation    Basic usage examples for RobotFrameworkPGP
Library          RobotFrameworkPGP

*** Test Cases ***
Simple Encryption And Decryption Example
    [Documentation]    Demonstrates basic text encryption and decryption
    [Tags]    example    basic
    
    # Generate a key pair
    ${fingerprint}    Generate Key Pair
    ...    email=alice@example.com
    ...    name=Alice Smith
    ...    key_length=2048
    ...    passphrase=alice_secret
    
    # Encrypt a message
    ${message}    Set Variable    This is a secret message for Alice!
    ${encrypted}    Encrypt Text
    ...    text=${message}
    ...    recipients=alice@example.com
    
    # Decrypt the message
    ${decrypted}    Decrypt Text
    ...    encrypted_text=${encrypted}
    ...    passphrase=alice_secret
    
    # Verify the message
    Should Be Equal    ${decrypted}    ${message}
    Log    Successfully encrypted and decrypted: ${message}

Multiple Recipients Example
    [Documentation]    Shows how to encrypt for multiple recipients
    [Tags]    example    multi-recipient
    
    # Generate key pairs for two users
    Generate Key Pair    bob@example.com    Bob Johnson    2048    bob_secret
    Generate Key Pair    carol@example.com    Carol Williams    2048    carol_secret
    
    # Create list of recipients
    @{recipients}    Create List    bob@example.com    carol@example.com
    
    # Encrypt message for both recipients
    ${secret_message}    Set Variable    Meeting at 3 PM in conference room B
    ${encrypted_message}    Encrypt Text
    ...    text=${secret_message}
    ...    recipients=${recipients}
    
    # Both recipients can decrypt the message
    ${bob_decrypted}    Decrypt Text    ${encrypted_message}    bob_secret
    ${carol_decrypted}    Decrypt Text    ${encrypted_message}    carol_secret
    
    Should Be Equal    ${bob_decrypted}    ${secret_message}
    Should Be Equal    ${carol_decrypted}    ${secret_message}
    Log    Both Bob and Carol can read the message

Digital Signature Example
    [Documentation]    Demonstrates digital signatures
    [Tags]    example    signature
    
    # Generate a key pair for signing
    Generate Key Pair    david@example.com    David Brown    2048    david_secret
    
    # Create and sign a message
    ${document}    Set Variable    I hereby authorize the payment of $1000.
    ${signed_document}    Sign Text
    ...    text=${document}
    ...    key_id=david@example.com
    ...    passphrase=david_secret
    
    # Verify the signature
    ${verification}    Verify Signature    ${signed_document}
    Should Be True    ${verification}[valid]
    Log    Signature verified successfully
    Log    Signed by: ${verification}[username]

Symmetric Encryption Example
    [Documentation]    Shows password-based encryption (no keys needed)
    [Tags]    example    symmetric
    
    ${confidential_data}    Set Variable    Employee salary data: John Doe - $50000
    ${password}    Set Variable    company_secret_2023
    
    # Encrypt with password only
    ${encrypted_data}    Create Symmetric Encryption
    ...    text=${confidential_data}
    ...    passphrase=${password}
    
    # Decrypt with the same password
    ${decrypted_data}    Decrypt Text
    ...    encrypted_text=${encrypted_data}
    ...    passphrase=${password}
    
    Should Be Equal    ${decrypted_data}    ${confidential_data}
    Log    Symmetric encryption successful

*** Keywords ***
# Add any custom keywords here if needed