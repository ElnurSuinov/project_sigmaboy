import telebot

bot = telebot.TeleBot(token="TOKEN")
chat_id = "CHAT_ID"

def send_order_to_tg(order_text):
    bot.send_message(chat_id, order_text, parse_mode="HTML")
