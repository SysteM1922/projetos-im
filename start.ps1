Set-Location -Path .\IM
Start-Process -FilePath .\start.bat

Set-Location -Path ..\FusionEngine
Start-Process -FilePath .\start.bat

Set-Location -Path ..\GenericGesturesModality-2023
Start-Process -FilePath .\GenericGesturesModality.exe

Set-Location -Path ..\WebAppAssistantV2
Start-Process -FilePath .\start_web_app.bat
Set-Location -Path ..
Start-Process "chrome.exe" "https://127.0.0.1:8082/index.htm"

.\venv\Scripts\activate

Set-Location -Path .\app
python.exe main.py