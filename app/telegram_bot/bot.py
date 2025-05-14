import threading
import telebot
from config import Config


bot  = telebot.TeleBot(Config.TELEGRAM['token'])
@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Привет!')