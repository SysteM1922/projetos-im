from driver import Driver
import websockets
import ssl
import asyncio
import json

HOST = "localhost"

def process_message(message: str):
    if message == "OK":
        return "OK"
    else:
        json_message = json.loads(message)
        print("Command: ", json_message["text"])
        return json_message

async def message_handler(driver: Driver, message: str):
    message = process_message(message)
    print(f"Received message: {message}")

async def main():

    driver = Driver()
    driver.reject_cookies()

    mmi_cli_out_add = f"wss://{HOST}:8005/IM/USER1/APP"

    # SSL config
    ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        async with websockets.connect(mmi_cli_out_add, ssl=ssl_context) as websocket:
            print("Connected to WebSocket")

            while True:
                message = await websocket.recv()
                await message_handler(driver, message)
    
    except Exception as e:
        print(f"Error: {e}")

    driver.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())