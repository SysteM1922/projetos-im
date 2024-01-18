# projeto-im
<h1>Projeto da Unidade Curricular de Interação Multimodal 2023/2024</h1>
<h2>103668 Gonçalo Rodrigues Silva<br>
103600 Guilherme Costa Antunes
</h2>
| Projeto | 1 | 2 | 3 |
| Nota | 18 | 18 | 17 |

## Requirements
- Chrome
- MS Edge
- Python 3.10
- Conexão à Internet

## How to setup
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
Caso contrário será necessário correr 5 terminais diferentes com os seguintes comandos:
```bat
cd .\IM\
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
cd .\GenericGesturesModality-2023\
.\GenericGesturesModality.exe
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
Para conversar com o site encontra-se um icon de microfone na aba MS Edge que deve abrir no link https://127.0.0.1:8082/index.htm e que deve ser pressionado cada vez que se quer enviar uma nova fala. A ativação do microfone também funciona ao pressionar a barra de espaço, quando selecionado o navegador.
## Possible Bugs
- ATENÇÃO: Os gestos foram gravados e treinados para um grupo pequeno de pessoas pelo que podem não ser reproduzíveis por qualquer pessoa
- Se não aparecer uma janela preta dentro do GenericGesturesModality verificar se o Kinect está corretamente conectado
- Se a conexão do Kinect for extremamente instável abrir o Painel de Controlo > Hardware e Som > Som > Gravação > Xbox NUI Sensor (Propriedades) > Níveis e reduzir para 0 o nível do Conjunto de Microfones (Windows 11)
- Se não houver feedback de voz ao iniciar o programa experimentar enviar um comando de voz pelo microfone ou fazer refresh da página, o feedback deverá voltar na próxima oportunidade. Pode reiniciar o último processo python para testar. Caso o bug persista reiniciar o computador.
- Caso o microfone esteja a captar mal ou nenhum som verificar se o dispositivo de entrada padrão não foi alterado indevidamente para o XBox NUI Sensor
- Caso existam problemas de CORS na aba do MS Edge que tem o microfone deve-se certificar que todos os terminais correram em powershell e não em cmd. É possível que o conda não seja ativável na powershell, recomendando-se a instalação de um virtual environment normal de python 3.10.
