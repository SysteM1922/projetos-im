# projeto-im
Projetos da Unidade Curricular de Interação Multimodal 2023/2024

## Requirements
- Chrome
- Python 3.10
- Conexão à Internet

## How to setup
- Extrair da pasta DemoMMI.zip as pastas FusionEngine e mmiframeworkV2<p>ATENÇÂO: NÃO SUBSTITUIR AS PASTAS rasaDemo e WebAppAssistantV2</p>
- Criar um venv

```bat
py -3.10 -m venv venv
```
- Ativar o venv

```bat
.\venv\Scripts\activate
```
- Instalar os requirements

```bat
pip install -r .\requirements.txt
```
- Treinar o Rasa

```bat
cd rasaDemo
rasa train
```

Caso esteja a ser usado um virtual environment conda deve substituir-se o comando de ativação em todos os lugares onde se encontrar o seguinte comando, incluindo o start.ps1:
```bat
.\venv\Scripts\activate
```

## How to run
Pode iniciar os módulos de comunicação na powershell com o comando
```bat
.\start.ps1
```
Caso contrário será necessário correr 4 terminais diferentes com os seguintes comandos:
```bat
cd .\mmiframeworkV2\
.\start.bat
```
```bat
cd .\FusionEngine\
.\start.bat
```
```bat
.\venv\Scripts\activate
cd rasaDemo
rasa run --enable-api -m .\models\ --cors “*”
```
```bat
cd .\WebAppAssistantV2\
.\start_web_app.bat
```
Quando o terminal Rasa imprimir a terceira linha azul com:
```python3
INFO     root  - Rasa server is up and running
```
O seguinte comando deve ser corrido num novo terminal:
```bat
py .\app\main.py
```
Para conversar com o site encontra-se um icon de microfone na aba chrome que foi aberta automaticamente no link https://127.0.0.1:8082/index.htm, que deve ser pressionado cada vez que se quer enviar uma nova fala. A ativação do microfone também funciona ao pressionar a barra de espaço, quando selecionado o navegador.
## Possible Bugs
- Se não houver feedback de voz ao iniciar o programa experimentar enviar um comando de voz pelo microfone, o feedback deverá voltar na próxima oportunidade. Pode reiniciar o último processo python para testar. Caso o bug pressista reiniciar o computador.
- Caso existam problemas de CORS na aba do Chrome que tem o microfone deve experimentar-se noutro navegador, como o Edge. Caso o problema persista certificar que todos os terminais correram em powershell e não em cmd. É possível que o conda não seja ativável na powershell, recomendando-se a instalação de um virtual environment python normal.
