from driver import Driver
import websockets
import ssl
import asyncio
import xml.etree.ElementTree as ET
import json

HOST = "127.0.0.1:8005"

stop_words = set(["procurar", "pesquisar", "produto", "por", "um", "uma" "comprar", "procura", "pesquisa", "compra", "para"])

bag_of_words = []

def process_message(message: str):
    if message == "OK":
        return "OK"
    else:
        json_command = ET.fromstring(message).find(".//command").text
        command = json.loads(json_command)["nlu"]
        return json.loads(command)

async def message_handler(driver: Driver, message: str):
    message = process_message(message)
    print(f"Message: {message}")

    if message == "OK":
        pass
    elif message["intent"]["name"]:
        if message["intent"]["name"] == "return":
            driver.return_to_previous_page()
        elif message["intent"]["name"] == "scroll":
            if message["entities"][0]["value"] == "cima":
                driver.scroll_up()
            elif message["entities"][0]["value"] == "baixo":
                driver.scroll_down()
        elif message["intent"]["name"] == "add_to_cart":
            driver.add_to_cart()
        elif message["intent"]["name"] == "search_product":
            words = message["text"].lower().split()
            for idx in range(len(words)-1, -1, -1):
                if words[idx] in stop_words:
                    driver.search_product(" ".join(words[idx+1:]))
                    return
            driver.search_product(message["text"])
        elif message["intent"]["name"] == "see_cart":
            driver.see_cart()
                

    else:
        print("Command not found")

async def main():

    driver = Driver()

    mmi_cli_out_add = f"wss://{HOST}/IM/USER1/APP"

    # SSL config
    ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE


    async with websockets.connect(mmi_cli_out_add, ssl=ssl_context) as websocket:
        print("Connected to WebSocket")

        while True:
            message = await websocket.recv()
            await message_handler(driver, message)

    driver.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())