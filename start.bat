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