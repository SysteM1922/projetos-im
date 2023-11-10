cd mmiframeworkV2
start .\start.bat

cd ..\FusionEngine
start .\start.bat

cd ..
call .\venv\Scripts\activate
cd rasaDemo
start rasa run --enable-api -m .\models\ --cors “*”

cd ..\WebAppAssistantV2
start .\start_web_app.bat

start microsoft-edge:https://127.0.0.1:8082/index.htm