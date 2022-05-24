import requests
import time
import telegram
from datetime import datetime
from config import *

DRAW_URL = "https://luckydraw.gamehub.garena.tw/service/luckydraw/"
GAME = "lol"
REGION = "TW"
VERSION = "1653292834"


def sendMessage(message: str):
    bot.send_message(text=message, chat_id=TELEGRAM_ID)


def queryExpiry(quite: bool = True) -> int:
    response = requests.get(
        DRAW_URL, {"sk": SK, "region": REGION, "tid": TID}, verify=False
    ).json()

    if "result" in response:
        result = response["result"]["cooldown_expiry"]
        print(result)
        if result == 0:
            result = int(time.time())

        if not quite:
            sendMessage(datetime.fromtimestamp(result).__str__())

        return result
    else:
        return int(time.time())


def draw() -> int:
    response = requests.post(
        DRAW_URL,
        {"game": GAME, "sk": SK, "region": REGION, "version": VERSION, "tid": TID},
        verify=False,
    ).json()

    if "result" in response:
        price = response["result"]["prize"]["item"]["desc"]
        print(price)
        sendMessage(price)
        return response["result"]["cooldown_expiry"]
    else:
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
