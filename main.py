import os
import sys
import subprocess
import base64
from flask import Flask, render_template

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

app = Flask(__name__, template_folder=resource_path('templates'))

def execute_ps(command):
    b64_cmd = base64.b64encode(command.encode('utf-16le')).decode('utf-8')
    inner_args = f"'-NoProfile', '-EncodedCommand', '{b64_cmd}'"

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = 0

    full_command = f'powershell -NoProfile -ExecutionPolicy Bypass -Command ...'

    subprocess.run(full_command, startupinfo=startupinfo, shell=False)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)