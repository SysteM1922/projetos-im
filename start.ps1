Set-Location -Path .\mmiframeworkV2
Start-Process -FilePath .\start.bat

Set-Location -Path ..\FusionEngine
Start-Process -FilePath .\start.bat

Set-Location -Path ..
.\venv\Scripts\activate
#conda activate rasa-env
Set-Location -Path .\rasaDemo
Start-Process -FilePath rasa -ArgumentList 'run', '--enable-api', '-m', '.\models\', '--cors', '*'

Set-Location -Path ..\WebAppAssistantV2
Start-Process -FilePath .\start_web_app.bat
Set-Location -Path ..
Start-Process "chrome.exe" "https://127.0.0.1:8082/index.htm"