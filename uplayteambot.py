# -*- coding: utf-8 -*-
# https://www.codementor.io/garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay
# Dependencies: Python 2.7.9, PIP 9.0.1, pip install requests

import sys
import json
import requests
import time
import urllib
import random

TOKEN = "299403003:AAFt3wfrfdPHorltacSJaS_NgtQwB1cbUyU"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
HEALTH_KEYWORDS = ["feel bad", "sick", "feeling bad", "home today", "stay at home", "off work", "off today", "cold", "temperature", "not feeling good", " ill ", " ill", "illness", "sickness"]
LATE_KEYWORDS = ["late", "traffic", "traffic jam", "later", "overslept"]
MY_MESSAGE = "Oh no, someone is not feeling good! We all wish you fast and healthy recovery. Get well soon!"
STICKERS_LATE = [ "CAADAgADVQEAAgeGFQdvd13tC031dAI", "CAADAgADegUAAhhC7gigZ-6cVjpUHAI", "CAADAgAEAgACIIEVAAFkPJOIJqVysQI", "CAADAgADpAIAAmMr4gl6TEALE3PBxAI" ]
STICKERS_HEALTHY = [ "CAADAgAD7AEAAs9fiwdjtP9oVunQtQI" ]


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    try:
        text = updates["result"][last_update]["message"]["text"]
    except KeyError as ke:
        print(ke)
        text = ""
    except IndexError as ie:
        print(ie)
        text = ""
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
#    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def send_sticker(sticker, chat_id):
    url = URL + "sendSticker?sticker={}&chat_id={}".format(sticker, chat_id)
    get_url(url)

def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            for trigger in HEALTH_KEYWORDS:
                if trigger in text.lower():
                    send_message(MY_MESSAGE, chat)
                    send_sticker(random.choice(STICKERS_HEALTHY), chat)
                    break
            for keyword in LATE_KEYWORDS:
                if keyword in text.lower():
                    send_sticker(random.choice(STICKERS_LATE), chat)
                    break
        except Exception as e:
            print(e)

text, chat = get_last_chat_id_and_text(get_updates())
#send_message(text, chat)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
