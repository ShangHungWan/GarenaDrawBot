import requests
import time
import telegram
from datetime import datetime
from config import *

DRAW_URL = "https://luckydraw.gamehub.garena.tw/service/luckydraw/"
GAME = "lol"
REGION = "TW"

version = ""

def sendMessage(message: str):
    bot.send_message(text=message, chat_id=TELEGRAM_ID)


def queryExpiry(quite: bool = True) -> int:
    global version

    response = requests.get(
        DRAW_URL, {"sk": SK, "region": REGION, "tid": TID},
    ).json()

    if "result" in response:
        result = response["result"]["cooldown_expiry"]
        version = response["result"]["settings"][0]["version"]
        print(f"next expiry: {result} = {datetime.fromtimestamp(result)}")
        if result == 0:
            result = int(time.time())

        if not quite:
            sendMessage(datetime.fromtimestamp(result).__str__())

        return result
    else:
        return int(time.time())


def draw() -> int:
    global version

    response = requests.post(
        DRAW_URL,
        {"game": GAME, "sk": SK, "region": REGION, "version": version, "tid": TID},
    ).json()

    if "result" in response:
        price = response["result"]["prize"]["item"]["desc"]
        print(f"price: {price}")
        sendMessage(price)
        return response["result"]["cooldown_expiry"]
    elif "error" in response:
        detail = response["detail"]
        print(f"error: {detail}")
        sendMessage(response["detail"])

        # get new version and draw again
        if detail == 'Luckydraw Version Error':
            queryExpiry()
            return draw()

        exit()
    else:
        print(f"exception: {response}")
        return queryExpiry()


def main():
    cooldown = queryExpiry()

    while True:
        if cooldown <= time.time():
            cooldown = draw()
        time.sleep(10)


if __name__ == "__main__":
    bot = telegram.Bot(TELEGRAM_BOT_TOKEN)
    main()
