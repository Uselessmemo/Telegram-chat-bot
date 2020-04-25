import requests
import json
import datetime
from time import sleep
from key import key


class BotHandler:
    def __init__(self,token):
        self.token=key
        self.api_url=f'https://api.telegram.org/bot{key}/'

    def get_updates_json(self, timeout = 100, offset = None):
        params = {'timeout': timeout, 'offset': offset}
        response=requests.get(self.api_url + 'getUpdates', params = params)
        return response.json()['result']

    def send_msg(self, chat_id, text):
        params={'chat_id' : chat_id, 'text' : text}
        response=requests.get(self.api_url + 'sendMessage', params = params)
        return response

    def last_update(self):
        res = self.get_updates_json()
        if len(res) > 0:
            last_update = res[-1]
        else:
            last_update = res[len(res)]
        return last_update

greet_bot = BotHandler(key)  
greetings = ('здравствуй', 'привет', 'ку', 'здорово')  
now = datetime.datetime.now()

def main():  
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.get_updates_json(new_offset)

        last_update = greet_bot.last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
            greet_bot.send_msg(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
            greet_bot.send_msg(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
            greet_bot.send_msg(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))
            today += 1

        new_offset = last_update_id + 1

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()