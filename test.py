import telebot
import os
from openai import OpenAI

from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, filters



BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def get_voice(update: Update, context: CallbackContext) -> None:
    # get basic info about the voice note file and prepare it for downloading
    new_file = context.bot.get_file(update.message.voice.file_id)
    # download the voice note as a file
    new_file.download(f"voice_note.ogg")

updater = Updater(BOT_TOKEN)

# Add handler for voice messages
updater.dispatcher.add_handler(MessageHandler(filters.voice , get_voice))

updater.start_polling()
updater.idle()



