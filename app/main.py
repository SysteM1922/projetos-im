from driver import Driver
import websockets
import ssl
import asyncio
import xml.etree.ElementTree as ET
import json

HOST = "127.0.0.1:8005"

stop_words = set(["procurar", "pesquisar", "produto", "por", "um",
                 "uma" "comprar", "procura", "pesquisa", "compra", "para"])
numeros = {"um": 1, "uma": 1, "dois": 2, "duas": 2, "três": 3, "tres": 3,
           "quatro": 4, "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9}

filters = {"Relevância": 1, "promoções": 2, "Promoção": 2, "nomes": 3, "Nome": 3, "Preço baixo": 4, "Preço crescente": 4,
           "Preço mais baixo": 4, "Preço decrescente": 5, "Preço alto": 5, "Preço mais alto": 5 }


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

        elif intent == "scroll":
            if message["entities"][0]["value"] == "cima":
                driver.scroll_up()

            elif message["entities"][0]["value"] == "baixo":
                driver.scroll_down()

        elif intent == "add_to_cart":
            if len(message["entities"]) > 0:
                qty_init = message["entities"][0]["value"]
                if qty_init in numeros:
                    qty = numeros[qty_init]
                else:
                    qty = int(qty_init)
                driver.add_to_cart(qty)

        elif intent == "search_product":
            words = message["text"].lower().split()

            for idx in range(len(words)-1, -1, -1):
                if words[idx] in stop_words:
                    driver.search_product(" ".join(words[idx+1:]))
                    return

            driver.search_product(message["text"])

        elif intent == "see_cart":
            driver.see_cart()

        elif intent == "filter_items":
            if len(message["entities"]) > 0:
                filter = message["entities"][0]["value"]
                if filter.lower() in [x.lower() for x in filters.keys()]:
                    driver.filter_items(filters[filter])
            else:
                driver.filter_items("")
        
        elif intent == "checkout":
            driver.checkout()

        elif intent == "quit":
            global not_quit
            not_quit = False

    else:
        print("Command not found")


async def main():

    driver = Driver()

    mmi_cli_out_add = f"wss://{HOST}/IM/USER1/APP"

    # SSL config
    ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        async with websockets.connect(mmi_cli_out_add, ssl=ssl_context) as websocket:
            print("Connected to WebSocket")

            while not_quit:
                try:
                    message = await websocket.recv()
                    await message_handler(driver, message)
                except:
                    pass

    except Exception as e:
        print(e)

    driver.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
