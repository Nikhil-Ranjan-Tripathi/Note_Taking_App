import speech_recognition as sr
import gtts
from playsound import playsound
import os
from datetime import datetime
from notion import NotionClient
r = sr.Recognizer()
token = "Your Taken ID"
database_id = 'Your DB ID'
client = NotionClient(token, database_id)

ACTIVATION_COMMAND = 'hey friday'

def get_audio():
    with sr.Microphone() as source:
        print("Say something")
        audio = r.listen(source)
    return audio      

def audio_to_text(audio):
    text=""
    try:
        text = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
    except sr.RequestError:
        print("could not request results from API")
    return text

def play_sound(text):
    try:
        tts = gtts.gTTS(text)
        tempfile ="./temp.mp3"
        tts.save(tempfile) 
        playsound(tempfile) 
        os.remove (tempfile)
    except AssertionError:
        print("Could not play sound")

if __name__ == '__main__':
    while True:
        a = get_audio()
        command = audio_to_text(a)
        if ACTIVATION_COMMAND in command.lower():
            print("ACTIVATED")
            play_sound("What can i do for you?")
            note = get_audio()
            note = audio_to_text(note)
            if note:
                play_sound(note)
                now = datetime.now().astimezone().isoformat()
                res = client.create_page(note, now, status="Active")
                if res.status_code == 200:
                    play_sound("Stored new item")
