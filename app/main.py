import random
from driver import Driver
import websockets
import asyncio
import xml.etree.ElementTree as ET
import json
import difflib
import ssl
import time
from tts import TTS
import re
from unidecode import unidecode
from enums import Type, Direction

HOST = "127.0.0.1:8005"
OUTPUT = "127.0.0.1:8000"

stop_words = ["procurar", "pesquisar", "produto", "por", "um", "uma" "comprar",
              "procura", "pesquisa", "compra", "para", "quero", "querer", "pelas",
              "pelos", "os", "as", "o", "a", "pelo", "pela", "detalhes", "abrir", "ver", "sobre"]

remove_words = ["remover", "retirar", "tirar", "apagar", "eliminar", "produto", "do", "carrinho", "de", "compras"]

sorts = {"Relevância": 1, "Promoção": 2, "Nome": 3, "Preço mais baixo": 4, "preço mais alto": 5 }

stores = {"Pingo Doce": 1, "Pingo Doce Madeira": 2, "Pingo Doce Solmar": 3, "Mercadão Solidário": 4, "Saúde": 5, "Medicamentos": 6 }

help_options = ["carrinho", "produto", "código postal", "morada", "loja", "operações", "todas"]

not_found = ["Desculpe, não percebi o que disse, pode repetir?", "Não percebi, pode repetir?", "Não percebi, pode repetir por favor?"
             "Desculpe não percebi o que disse, tente dizer mais devagar", "Não percebi, pode repetir mais devagar por favor?",
             "Não consegui entender, pode repetir?", "Desculpe não entendi, pode repetir?", "Não entendi, pode repetir por favor?",
             "Não consegui perceber, experimente dizer mais devagar", "Não percebi, pode repetir mais devagar por favor?", "Pode repetir por favor?"]

categories_list = []

with open("app\categorias.txt", "r", encoding="utf-8") as f:
    for line in f:
        categories_list.append(line.strip())

def process_message(message: str):

    if message == "OK":
        return message, Type.OK
    
    commands = ET.fromstring(message).findall(".//command")
    json_command = commands.pop(0).text
    command = json.loads(json_command)
    modality = command["recognized"][0]
    
    if modality == "SPEECH":
        return json.loads(command["nlu"]), Type.SPEECH
    elif modality == "GESTURES":
        return command["recognized"][1], Type.GESTURE
    elif modality == "FUSION":
        return (command["recognized"][1:], commands), Type.FUSION

async def message_handler(driver: Driver, message: str):

    message, typ = process_message(message)

    if typ == Type.SPEECH:
        speech_control(driver, message)
    elif typ == Type.GESTURE:
        gesture_control(driver, message)
    elif typ == Type.FUSION:
        fusion_control(driver, message)
    elif typ == Type.OK:
        return

def speech_control(driver: Driver, message: dict):

    def command_not_found():
        not_found_msg = random.choice(not_found)
        driver.sendToVoice(not_found_msg)
        print("Command not found")

    if message == None:
        return
    
    elif message["intent"]["name"]:
        intent = message["intent"]["name"]
        print("SPEECH:", intent.upper())

        if message["intent"]["confidence"] < 0.6:
            command_not_found()

        elif intent == "return":
            driver.return_to_previous_page()

        elif intent == "affirm":
            driver.affirm()

        elif intent == "insert_number":
            if len(message["entities"]) > 0:
                numbers = [message["entities"][i]["value"] for i in range(len(message["entities"])) if message["entities"][i]["extractor"] == "DIETClassifier"]
                driver.insert_number(numbers)

        elif intent == "clear_text":
            driver.clear_text()

        elif intent == "scroll":
            if len(message["entities"]) > 0:
                if message["entities"][0]["value"] == "1":
                    driver.scroll_up()

                elif message["entities"][0]["value"] == "0":
                    driver.scroll_down()

        elif intent == "add_to_cart":
            if len(message["entities"]) > 0:
                qty_init = 0
                for entity in message["entities"]:
                    if entity["extractor"] == "DIETClassifier":
                        qty_init = entity["value"]
                        break
                driver.add_to_cart(int(qty_init))
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

            if driver.is_cart_open():

                product = message["text"].lower().split()
                for word in remove_words:
                    sim = difflib.get_close_matches(word, product, n=1, cutoff=0.8)
                    if sim:
                        product.remove(sim[0])
                product = " ".join(product)

                products_list = driver.get_cart_products()

                for p in products_list:
                    for word in remove_words:
                        sim = difflib.get_close_matches(word, p[0].lower().split(), n=1, cutoff=0.8)
                        if sim:
                            p[0].replace(sim[0], "")

                products_list = [[re.sub(r'[^a-zA-Z0-9\s]+', '', unidecode(x[0])).strip(), x[1]] for x in products_list]
                print("Aqui1")
                sim = difflib.get_close_matches(unidecode(product), [x[0] for x in products_list], n=1, cutoff=0.3)[0]

                if sim:
                    driver.remove_from_cart(products_list[[x[0] for x in products_list].index(sim)][1], sim)
                else:
                    driver.sendToVoice("Não percebi o nome do produto, pode repetir?")
            else:
                driver.sendToVoice("É necessário abrir o carrinho para efectuar esta operação")

        elif intent == "open_product":
            products = {re.sub(r'[^a-zA-Z0-9\s]', '', unidecode(x.text.lower())).strip(): x for x in driver.get_visible_products()}
            words = message["text"].lower().split()
            
            input_word = None
            for idx in range(len(words)-1, -1, -1):
                if words[idx] in stop_words:
                    input_word = words[idx+1:]
                    break
            if input_word:
                input_word = " ".join(input_word)
                sim = difflib.get_close_matches(unidecode(input_word), list(products.keys()), n=1, cutoff=0.2)[0]
                if sim:
                    driver.open_product(sim, products[sim])
                else:
                    driver.sendToVoice("Não percebi o nome do produto, pode repetir?")
            else:
                driver.sendToVoice("Não percebi o nome do produto, pode repetir?")

        
        elif intent == "checkout":
            driver.checkout()

        elif intent == "change_store":
            lst = [entity for entity in message["entities"] if entity["entity"] == "store"]
            if len(lst) > 0:
                store = lst[0]["value"]
                store = stores.get(store, None)
                if store:
                    driver.change_store(store)
                else:
                    driver.sendToVoice("Não percebi o nome da loja, pode repetir?")
            else:
                driver.change_store()

        elif intent == "change_category":
            if len(message["entities"]) > 0:
                category = None
                for entity in message["entities"]:
                    if entity["extractor"] == "RegexEntityExtractor":
                        category = entity["value"].lower()
                        break
                if not category:
                    try:
                        category = message["entities"][0]["value"].lower()
                    except:
                        driver.sendToVoice("Não percebi a categoria, pode repetir?")
                        return
                cat = difflib.get_close_matches(category, categories_list, n=1, cutoff=0.6)[0]
                if cat:
                    driver.change_category(cat)
                else:
                    driver.sendToVoice("Não percebi a categoria, pode repetir?")

        elif intent == "change_zip_code":
            driver.open_zip_code()

        elif intent == "sort_items":
            if len(message["entities"]) > 0:
                sort_opt = message["entities"][0]["value"]
                if sort_opt in sorts:
                    driver.sort_items(sorts[sort_opt])
            else:
                driver.sort_items()

        elif intent == "filter_products":
            position = None
            filter_opt = None
            if len(message["entities"]) > 0:
                for entity in message["entities"]:
                    if entity["entity"]=="number" and entity["extractor"] == "DIETClassifier":
                        position = entity["value"]
                    elif entity["entity"]=="filter_type":
                        filter_opt = entity["role"]
            driver.filter_products(filter_opt, position)

        elif intent == "choose_position":
            if len(message["entities"]) > 0:
                for entity in message["entities"]:
                    if entity["entity"]=="number" and entity["extractor"] == "DIETClassifier":
                        driver.choose_position(entity["value"])
                        break
            else:
                driver.choose_position()

        elif intent == "help":
            if len(message["entities"]) > 0:
                for entity in message["entities"]:
                    if entity["entity"]=="help_option" and entity["extractor"] == "DIETClassifier":
                        help_opt = entity["value"].lower()
                        break
                help_opt = difflib.get_close_matches(help_opt, help_options, n=1, cutoff=0.7)[0]
                if help_opt:
                    driver.help(help_opt)
                else:
                    driver.sendToVoice("Em que posso ajudar?")
            else:
                driver.help()

        elif intent == "quit":
            if driver.quit():
                global not_quit
                not_quit = False

    else:
        command_not_found()

def gesture_control(driver: Driver, message: str):
    print("Gesture:", message)
    
    if message == "CONTINENCE":
        if driver.quit():
            global not_quit
            not_quit = False

    elif message == "OPENL":
        driver.change_product_gestures(Direction.LEFT)

    elif message == "OPENR":
        driver.change_product_gestures(Direction.RIGHT)

    elif message == "PUSHF":
        driver.press()

    elif message == "RAISERH":
        driver.help_gestures()

    elif message == "SCROLLDL":
        driver.change_category_gestures(Direction.DOWN)

    elif message == "SCROLLDR":
        driver.scroll_up()

    elif message == "SCROLLUL":
        driver.change_category_gestures(Direction.UP)

    elif message == "SCROLLUR":
        driver.scroll_down()

    elif message == "TRANSPORTR":
        driver.add_to_cart()

def fusion_control(driver: Driver, message: str):
    command = message[0][0]
    print("Fusion:", " ".join(message[0]))
    
    if command == "QUIT":
        if driver.quit():
            global not_quit
            not_quit = False
    
    elif command == "SCROLL":
        if message[0][1] == "UP":
            driver.scroll_up()
        elif message[0][1] == "DOWN":
            driver.scroll_down()
    
    elif command == "OPEN_PRODUCT":
        driver.open_product_gestures()

    elif command == "HELP":
        if len(message[0]) > 1:
            help_option = message[0][1]
            if help_option == "CARRINHO":
                driver.help("carrinho")
            elif help_option == "PRODUTO" or help_option == "PRODUTOS":
                driver.help("produto")
            elif help_option == "CODIGO_POSTAL" or help_option == "MORADA":
                driver.help("morada")
            elif help_option == "LOJA":
                driver.help("loja")
            elif help_option == "OPERACOES":
                driver.help("operações")
            elif help_option == "GESTOS":
                driver.help("gestos")
            elif help_option == "TODAS":
                driver.help("todas")
        else:
            driver.help()
    
    elif command == "ADD_TO_CART":
        for c in message[1]:
            command = json.loads(c.text)
            if command["recognized"][0] == "SPEECH":
                nlu = json.loads(command["nlu"])
                for entity in nlu["entities"]:
                    if entity["extractor"] == "DIETClassifier":
                        driver.add_to_cart(int(entity["value"]))
                        break
                break

not_quit = True

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
