# pip install flask
# pip install flask-sqlalchemy
# pip install speechrecognition
# pip install PyAudio
# pip install gTTS

import speech_recognition as sprec
import time 
import os
import pygame
from gtts import gTTS

pygame.mixer.init()

def speech(lang="id-ID"):
    # persiapkan mic dan recognizernya
    mic = sprec.Microphone()
    recog = sprec.Recognizer()

    with mic as audio_file:
        recog.adjust_for_ambient_noise(audio_file) # untuk mengatasi noise
        audio = recog.listen(audio_file) # untuk mendengarkan apa yang di bicarakan
        return recog.recognize_google(audio, language=lang) # untuk recognisi

def speak_text(text, lang='id'):
    tts = gTTS(text=text, lang=lang) # untuk konver text ke suara
    filename = "response.mp3"
    tts.save(filename) # save hasil konversi ke mp3
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    time.sleep(0.1)  # Small delay to ensure the file is not in use
    os.remove(filename) # hapus file mp3 supaya jangan buat memori penuh..

if __name__ == "__main__":
    text = speech() # disimpan dalam variabel text
    speak_text(text)

