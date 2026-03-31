import os
import time
import sys
import requests
import subprocess

def run_update(download_url):
    # Wait for the main process to exit completely to avoid "file in use" errors
    time.sleep(3)

    try:
        # Download the new version of main.exe
        response = requests.get(download_url, timeout=60)

        if response.status_code == 200:
            # Clean up old temporary files if they exist
            if os.path.exists("main.exe.new"):
                os.remove("main.exe.new")

            # Write the downloaded content to a temporary file
            with open("main.exe.new", "wb") as f:
                f.write(response.content)

            # Replace the old executable with the new one
            if os.path.exists("main.exe"):
                os.remove("main.exe")

            os.rename("main.exe.new", "main.exe")

            # Start the newly updated application
            subprocess.Popen(["main.exe"])
        else:
            # If download fails, try to restart the original app
            if os.path.exists("main.exe"):
                subprocess.Popen(["main.exe"])

    except Exception:
        # Emergency restart of the original app if something goes wrong
        if os.path.exists("main.exe"):
            subprocess.Popen(["main.exe"])

    # Always exit the updater after completion or failure
    sys.exit()

if __name__ == "__main__":
    # Check if download URL was passed as a command-line argument
    if len(sys.argv) > 1:
        run_update(sys.argv[1])