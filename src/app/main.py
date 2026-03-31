import os
import sys
import subprocess
import base64
from flask import Flask, render_template, request
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(current_dir, "../../"))
load_dotenv(os.path.join(BASE_DIR, ".env"))

def get_template_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'templates')

    return os.path.abspath(os.path.join(os.path.dirname(current_dir), "templates"))

app = Flask(__name__, template_folder=get_template_path())

def execute_ps(command):
    """ Execute PowerShell command hidden """
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = 0

    encoded_command = base64.b64encode(command.encode('utf-16le')).decode('utf-8')
    full_command = f'powershell.exe -NoProfile -ExecutionPolicy Bypass -EncodedCommand {encoded_command}'

    subprocess.run(
        full_command,
        startupinfo=startupinfo,
        creationflags=subprocess.CREATE_NO_WINDOW,
        shell=False
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/off')
def internet_off():
    ps_script = "Remove-NetFirewallRule -DisplayName 'BlockInternet' -ErrorAction SilentlyContinue; New-NetFirewallRule -DisplayName 'BlockInternet' -Direction Outbound -Action Block -RemoteAddress Internet"
    execute_ps(ps_script)
    return "Command sent: Disable"

@app.route('/on')
def internet_on():
    ps_script = "Remove-NetFirewallRule -DisplayName 'BlockInternet' -ErrorAction SilentlyContinue"
    execute_ps(ps_script)
    return "Command sent: Enable"

@app.route('/trigger-update', methods=['POST'])
def trigger_update():
    """ Endpoint to receive update notification """
    data = request.json
    expected_password = os.getenv("UPDATE_PASSWORD")

    if data and data.get('password') == expected_password:
        update_url = data.get('url', f"http://{os.getenv('MY_IP')}:8000/main.exe")
        # Start the external updater and exit
        subprocess.Popen(["update.exe", update_url])
        os._exit(0)

    return "Unauthorized", 401

if __name__ == '__main__':
    env_port = os.getenv("FLASK_PORT")
    port = int(env_port) if env_port else 5000
    # Minimal notification that the server is running
    print(f" * Server running on port {port}")
    app.run(host='0.0.0.0', port=port)