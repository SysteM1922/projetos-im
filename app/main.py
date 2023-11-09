from driver import Driver
import websockets
import asyncio
import xml.etree.ElementTree as ET
import json
import nltk
import ssl
from tts import TTS

HOST = "127.0.0.1:8005"
OUTPUT = "127.0.0.1:8000"

stop_words = set(["procurar", "pesquisar", "produto", "por", "um",
                 "uma" "comprar", "procura", "pesquisa", "compra", "para", "quero", "querer"])

numeros = {"um": 1, "uma": 1, "dois": 2, "duas": 2, "três": 3, "tres": 3,
           "quatro": 4, "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9}

filters = {"relevância": 1, "promoções": 2, "promoção": 2, "nomes": 3, "nome": 3, "preço baixo": 4, "preço crescente": 4,
           "preço mais baixo": 4, "preço decrescente": 5, "preço alto": 5, "preço mais alto": 5 }

stores = {"pingo Doce": 1, "madeira": 2, "pingo doce madeira": 2, "sol mar": 3,"solmar": 3,"pingo doce solmar": 3, "pingo doce sol mar": 3, "pingo doce açores": 3, "açores": 3, "mercadão solidário": 4, "saúde": 5, "medicamentos": 6 }

not_quit = True

def process_message(message: str):
    if message == "OK":
        return "OK"
    else:
        json_command = ET.fromstring(message).find(".//command").text
        command = json.loads(json_command)["nlu"]
        return json.loads(command)

async def message_handler(driver: Driver, message: str):
    message = process_message(message)
    print(f"Message: {message['text']}")

    if message == "OK":
        pass

    elif message["intent"]["name"]:
        intent = message["intent"]["name"]

        if intent == "return":
            driver.return_to_previous_page()

        elif intent == "affirm":
            driver.affirm()

        elif intent == "insert_number":
            if len(message["entities"]) > 0:
                numbers = [message["entities"][i]["value"].lower() for i in range(len(message["entities"]))]
                numbers = [numeros[x] if x in numeros else x for x in numbers]
                driver.insert_number(numbers)

        elif intent == "clear_text":
            driver.clear_text()

        elif intent == "scroll":
            if len(message["entities"]) > 0:
                if message["entities"][0]["value"] == "cima":
                    driver.scroll_up()

                elif message["entities"][0]["value"] == "baixo":
                    driver.scroll_down()

        elif intent == "add_to_cart":
            if len(message["entities"]) > 0:
                qty_init = message["entities"][0]["value"].lower()
                if qty_init in numeros:
                    qty = numeros[qty_init]
                else:
                    qty = int(qty_init)
                driver.add_to_cart(qty)
            else:
                driver.add_to_cart()

        elif intent == "search_product":
            words = message["text"].lower().split()

            for idx in range(len(words)-1, -1, -1):
                if words[idx] in stop_words:
                    driver.search_product(" ".join(words[idx+1:]))
                    return

            driver.search_product(message["text"])

        elif intent == "open_cart":
            driver.open_cart()

        elif intent == "close_cart":
            driver.close_cart()

        elif intent == "clear_cart":
            driver.clear_cart()

        elif intent == "remove_from_cart":
            driver.remove_from_cart()
        
        elif intent == "checkout":
            driver.checkout()

        elif intent == "change_store":
            if len(message["entities"]) > 0:
                store = message["entities"][0]["value"].lower()
                if store in stores:
                    driver.change_store(stores[store])
            else:
                driver.change_store()

        elif intent == "change_zip_code":
            driver.open_zip_code()

        elif intent == "filter_items":
            if len(message["entities"]) > 0:
                filter = message["entities"][0]["value"].lower()
                if filter in filters:
                    driver.filter_items(filters[filter])
            else:
                driver.filter_items()

        elif intent == "quit":
            if driver.quit():
                global not_quit
                not_quit = False

    else:
        print("Command not found")


async def main():

    sendToVoice = TTS(FusionAdd=f"https://{OUTPUT}/IM/USER1/APPSPEECH").sendToVoice

    driver = Driver(sendToVoice)

    mmi_cli_out_add = f"wss://{HOST}/IM/USER1/APP"

    ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE


    async with websockets.connect(mmi_cli_out_add, ssl=ssl_context) as websocket: # ssl = ssl_context para ignorar certificado (menos seguro)
        print("Connected to WebSocket")

        while not_quit:
            try:
                message = await websocket.recv()
                await message_handler(driver, message)
            except Exception as e:
                print("Exception:",e)

    driver.close()
    exit(0)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
