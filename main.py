import requests
from lxml import html
import telebot, time

TOKEN = "1375344782:AAFqdxa-AERRVWNKixPtHfvySv9Kt-yDlLU"
bot = telebot.TeleBot(TOKEN)

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)

keyboard1.row('/hello', '/look_at_my_list')
keyboard1.row('/start')
keyboard1.row('/add_item', '/delete_item')


def check(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    # adding headers to show that you are
    # a browser who is sending GET request

    page = requests.get(url, headers=headers)
    for i in range(5):
        # because continuous checks in
        # milliseconds or few seconds
        # blocks your request
        time.sleep(10)

        # parsing the html content
        doc = html.fromstring(page.content)

        # checking availaility
        XPATH_AVAILABILITY = '//div[@id ="availability"]//text()'
        RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
        AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
        if AVAILABILITY == 'No disponible.' or AVAILABILITY == 'Disponible a través de estos vendedores.' or len(
                AVAILABILITY) > 100:
            AVAILABILITY = None
        return AVAILABILITY


@bot.message_handler(commands=["hello"])
def send_welcome(message):
    id_chat = message.chat.id
    bot.send_message(id_chat, "Hello. I`m amazon bot \n Fulfill the list and press start", reply_markup=keyboard1)


@bot.message_handler( commands= ["add_item"])
def add_item(message):
    id_chat = message.chat.id
    msg = bot.reply_to(message, 'Send me a link please')
    bot.register_next_step_handler(msg, add)

def add(message):
    items.append(message.text)


import threading
@bot.message_handler(commands=["start"])
def start(message):

    t = threading.Thread(target=handle, args=(message,))
    t.start()

def handle(message):
    id_chat = message.chat.id
    bot.send_message(id_chat, "Ok, I`m looking at items every 10 min", reply_markup=keyboard1)

    while True:

        time.sleep(600)

        for item in items:


            if check(item) != None :
                bot.reply_to(message, "I have something for you: \n" + item, reply_markup=keyboard1)
                items.remove(item)




@bot.message_handler( commands= ["delete_item"])
def delete_item(message):
    id_chat = message.chat.id
    msg = bot.reply_to(message, 'Send me the link please')
    bot.register_next_step_handler(msg, delete)


def delete(message):
    if message.text in items:
        items.remove(message.text)

    else:
        bot.reply_to(message, 'There`s not such link in the list')


@bot.message_handler( commands= ["look_at_my_list"])
def show_list(message):
    id_chat = message.chat.id
    list = open('list.txt', 'w')
    for item in items:
        msg = bot.reply_to(message, str(item))
        list.write(item + '\n')
    list.close()
    bot.reply_to(message, 'That`s all from the list \n I`ve save the list in a file')
    f = open("list.txt", "rb")
    bot.send_document(message.chat.id, f)
    f.close()




items=[]
while True:
    try:
        lists = open('list.txt')
        list = lists.read().splitlines()
        for item in list:
            items.append(item)
        print(items)
        lists.close()
        bot.polling()

    except Exception as e:
        print(e)
        time.sleep(60)
