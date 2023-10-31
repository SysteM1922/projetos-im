from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import websockets
import ssl
import asyncio

HOST = "localhost"

class Driver():

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.page = self.driver.get("https://www.mercadao.pt/store/pingo-doce")
        self.driver.maximize_window()

    def close(self):
        self.driver.close()

    def reject_cookies(self):
        try:
            button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id=\'onetrust-button-group\']/div[3]/button"))
            )
            button.click()
            self.driver.find_element(By.XPATH, "//div[@id=\'onetrust-pc-sdk\']/div/div[3]/div/button").click()   
        except TimeoutException:
            pass

async def im1_message_handler(message):
    # Implemente a lógica do manipulador de mensagens aqui
    print(f"Received message: {message}")

async def socket_open_handler():
    # Implemente a lógica do manipulador de abertura do socket aqui
    print("WebSocket is open")

async def main():

    driver = Driver()
    driver.reject_cookies()

    mmi_cli_out_add = f"wss://{HOST}:8005/IM/USER1/APP"

    ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with websockets.connect(mmi_cli_out_add, ssl=ssl_context) as websocket:
        print("Connected to WebSocket")

        while True:
            message = await websocket.recv()
            await im1_message_handler(message)

    driver.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())