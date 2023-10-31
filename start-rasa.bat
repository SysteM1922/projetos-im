call .\venv\Scripts\activate
cd rasaDemo
rasa run --enable-api -m .\models\ --cors “*”