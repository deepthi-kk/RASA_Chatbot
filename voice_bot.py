## Run this command in terminal  before executing this program
## rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
## and also run this in seperate terminal
## rasa run actions

import requests
import speech_recognition as sr     # import the library
import subprocess
import pyglet
import pygame
from gtts import gTTS
import os
from playsound import playsound
# sender = input("What is your name?\n")

bot_message = ""
message=""

r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": "Hi"})


while bot_message != "Bye" or bot_message!='thanks':

    r = sr.Recognizer()  # initialize recognizer
    with sr.Microphone() as source:  # mention source it will be either Microphone or audio files.
        print("Speak Anything :")
        audio = r.listen(source)  # listen to the source
        try:
            message = r.recognize_google(audio)  # use recognizer to convert our audio into text part.
            print("You said : {}".format(message))

        except:
            print("Sorry could not recognize your voice")  # In case of voice not recognized  clearly
    if len(message)==0:
        continue
    
    r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": message})
    print("Bot says, ",end=' ')
    for i in r.json():
        bot_message = i['text']
        print(f"{bot_message}")

    myobj = gTTS(text=bot_message)
    myobj.save("output.mp3")
    # Playing the converted file
    #subprocess.call("welcome.mp3",shell=True)
    #subprocess.call(['mpg321', "welcome.mp3", '--play-and-exit'],shell=True)

    
    # pyglet.lib.load_library('avbin64')
    # pyglet.have_avbin=True
    # song = pyglet.media.load('welcome.mp3')#your file name
    # song.play()
    # pyglet.app.run()
    #pygame.mixer.init()
    #pygame.mixer.music.load("welcome.mp3")
    #pygame.mixer.music.play()
    #pygame.mixer.music.stop()
    #os.remove("welcome.mp3")
    # pygame.mixer.init()
    # pygame.mixer.music.load("welcome.mp3")
    # pygame.mixer.music.set_volume(1)
    # pygame.mixer.music.play()
    # pygame.mixer.music.get_endevent()
    # while pygame.mixer.music.get_busy():
    #     continue
    # pygame.mixer.music.load("empty.mp3")
    # os.remove("welcome.mp3")
    playsound("output.mp3",True)
    os.remove("output.mp3")