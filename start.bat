:: Not working properly

cd mmiframeworkV2
start .\start.bat

cd ..
cd FusionEngine
start .\start.bat

cd ..
.\venv\Scripts\activate
cd rasaDemo
start rasa run --enable-api -m .\models\ --cors “*”

cd ..
cd WebAppAssistantV2
start .\start_web_app.bat