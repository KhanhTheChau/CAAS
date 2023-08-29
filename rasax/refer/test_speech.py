## Run this command in terminal  before executing this program
## rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
## and also run this in seperate terminal
## rasa run actions

import requests

import speech_recognition as sr
from gtts import gTTS
import os

def speak(text):
    print("AI: "+ text)
    tts=gTTS(text=text,lang='vi') 
    tts.save("D:\\project\\file_mp3\\sound.mp3")
    os.system("D:\\project\\file_mp3\\sound.mp3")
def get_audio():
    AI_ear= sr.Recognizer()
    while True:
        with sr.Microphone() as mic:
            print("AI: ")
            audio=AI_ear.record(mic,duration=5)
        try:
            you=AI_ear.recognize_google(audio,language="vi-VN")
            print("Tôi: " + you)
            return you
        except: continue

bot_message = ""
message=""

r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": "Xin chào"})

print("AI: ",end=' ')
for i in r.json():
    bot_message = i['text']
    print(f"{bot_message}")


while bot_message != "Bye":

    message = get_audio()
 
    r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": message})

    print("AI: ",end=' ')
    for i in r.json():
        bot_message = i['text']
        print(f"{bot_message}")
    speak(bot_message)

