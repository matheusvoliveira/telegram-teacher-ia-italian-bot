import telebot
import os
from openai import OpenAI
from teacher_instructions import teacher_instructions as teacher_instructions

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

@bot.message_handler(content_types=['voice'])
def get_voice(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("voice_note.ogg", 'wb') as f:
        f.write(downloaded_file)
    process_user_voice("voice_note.ogg", message)

def process_user_voice(voice_note, message):
    audio_file = open(voice_note, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    question = transcription.text 
    response_text, _ = generate_response(question)
    response_text, audio_content = generate_response(question)
    send_audio(message, audio_content)
    bot.reply_to(message, response_text)

@bot.message_handler(commands=['audio'])
def request_message_audio(message):
    question = message.text.replace('/audio', '').strip()
    if question:
        response_text, audio_content = generate_response(question)

        send_audio(message, audio_content)
        bot.reply_to(message, response_text)
    else:
        bot.reply_to(message, "Please provide a question after the /audio command.")

@bot.message_handler(func=lambda message: True)
def send_text_message(message):
    question = message.text
    response_text, _ = generate_response(question)
    bot.reply_to(message, response_text)

input_list = []
input_list.append({"role": "user", "content": teacher_instructions})

def generate_response(question):

    global input_list

    if len(input_list) >= 2 and input_list[-1]['content'] == input_list[-2]['content']:
        pass
    else:
        input_list.append({"role": "user", "content": question})
    print(input_list)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=input_list
    )
    
    if len(input_list) == 10:
        del input_list[1]

    response_text = response.choices[-1].message.content
    audio_content = response_text  
    return response_text, audio_content

def send_audio(message, audio_content):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=audio_content
    )
    with open("speech.mp3", 'wb') as f:
        f.write(response.content)

    with open("speech.mp3", "rb") as audio:
        bot.send_audio(message.chat.id, audio)

bot.polling(none_stop=True)


