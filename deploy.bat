@echo off
echo Running updater..
cd dist\InternetSwitcher
start "" send-update.exe
python -m http.server 8000