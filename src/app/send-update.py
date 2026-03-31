import os
import sys
import requests
from dotenv import load_dotenv

# Get the absolute path of the directory where send-update.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define project root (two levels up from src/tools/send-update.py)
BASE_DIR = os.path.abspath(os.path.join(current_dir, "../../"))

# Explicitly load .env from the project root
load_dotenv(os.path.join(BASE_DIR, ".env"))

def send_notification():
    target_ip = os.getenv("TARGET_IP")
    my_ip = os.getenv("MY_IP")
    flask_port = os.getenv("FLASK_PORT", "5000")
    password = os.getenv("UPDATE_PASSWORD")

    if not all([target_ip, my_ip, password]):
        print("Error: Missing configuration in .env file.")
        return

    url = f"http://{target_ip}:{flask_port}/trigger-update"
    payload = {
        "password": password,
        "url": f"http://{my_ip}:8000/main.exe"
    }

    try:
        response = requests.post(url, json=payload, timeout=5)

        if response.status_code == 200:
            print("Update signal sent successfully.")
        else:
            print(f"Update failed. Server returned status: {response.status_code}")

    except requests.exceptions.RequestException:
        print("Error: Could not connect to the target machine.")

if __name__ == "__main__":
    send_notification()