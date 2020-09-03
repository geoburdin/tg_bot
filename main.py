from lxml import html
import requests
from time import sleep
import telebot

TOKEN = "1375344782:AAFqdxa-AERRVWNKixPtHfvySv9Kt-yDlLU"
bot = telebot.TeleBot(TOKEN)

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('/start', '/add_item', '/delete_item', '/stop')
keyboard1.row('/look_at_my_list')

def check(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

    # adding headers to show that you are
        # a browser who is sending GET request
    page = requests.get(url, headers=headers)
    for i in range(20):
            # because continuous checks in
            # milliseconds or few seconds
            # blocks your request
        sleep(5)

                # parsing the html content
        doc = html.fromstring(page.content)

                # checking availaility
        XPATH_AVAILABILITY = '//div[@id ="availability"]//text()'
        RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
        AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
        return AVAILABILITY

items=[]

@bot.message_handler(commands=["start"])
def send_welcome(message):
    id_chat = message.chat.id
    bot.send_message(id_chat, "Hello. I`m amazon bot", reply_markup=keyboard1)


@bot.message_handler( commands= ["add_item"])
def add_item(message):
    id_chat = message.chat.id
    msg = bot.reply_to(message, 'Send me a link please')
    bot.register_next_step_handler(msg,add)


def add(message):
    items.append(message.text)


@bot.message_handler( commands= ["delete_item"])
def delete_item(message):
    id_chat = message.chat.id
    msg = bot.reply_to(message, 'Send me the link please')
    bot.register_next_step_handler(msg, delete)


def delete(message):
    items.remove(message.text)



@bot.message_handler( commands= ["stop"])
def stop_repeat(message):
    id_chat = message.chat.id
    bot.stop_bot()


@bot.message_handler( commands= ["look_at_my_list"])
def show_list(message):
    id_chat = message.chat.id
    for item in items:
        msg = bot.reply_to(message, str(item))


bot.polling()