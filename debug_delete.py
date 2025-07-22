#!/usr/bin/env python3
"""Debug script for key deletion issue."""

import tempfile
from src.RobotFrameworkPGP.pgp_library import RobotFrameworkPGP

def debug_delete():
    # Create temp directory
    temp_dir = tempfile.mkdtemp(prefix="debug_gpg_")
    print(f"Using temp directory: {temp_dir}")
    
    # Create library instance
    library = RobotFrameworkPGP(gnupg_home=temp_dir)
    
    # Generate key
    print("Generating key...")
    fingerprint = library.generate_key_pair(
        email="test@example.com",
        name="Test User", 
        key_length=1024,
        passphrase="testpassword"
    )
    print(f"Generated key: {fingerprint}")
    
    # List keys before deletion
    keys = library.list_keys()
    secret_keys = library.list_keys(secret=True)
    print(f"Keys before deletion: {len(keys)} public, {len(secret_keys)} secret")
    
    # Try to delete key
    print("Attempting to delete key...")
    try:
        library.delete_key("test@example.com", passphrase="testpassword")
        print("Delete operation completed")
    except Exception as e:
        print(f"Delete failed: {e}")
        return
    
    # List keys after deletion
    keys = library.list_keys()
    secret_keys = library.list_keys(secret=True)
    print(f"Keys after deletion: {len(keys)} public, {len(secret_keys)} secret")
    
    if len(keys) == 0:
        print("SUCCESS: Key was deleted")
    else:
        print("FAILURE: Key still exists")
        for key in keys:
            print(f"  Remaining key: {key}")

if __name__ == "__main__":
    debug_delete()