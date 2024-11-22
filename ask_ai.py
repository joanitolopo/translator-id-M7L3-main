# pip install transformers
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from googletrans import Translator
import speech_recognition as speech_recog
import time
from gtts import gTTS
import os
from playsound import playsound
import pygame


device = "cuda" # for GPU usage or "cpu" for CPU usage

# bisa ganti model agar lebih bagus (semakin besar semakin besar modelnya):
# indonlp/cendol-mt5-small-chat
# indonlp/cendol-mt5-base-chat
# indonlp/cendol-mt5-large-chat
# indonlp/cendol-mt5-xl-chat
# indonlp/cendol-mt5-xxl-merged-chat

checkpoint = "indonlp/cendol-mt5-small-chat"

tokenizer = AutoTokenizer.from_pretrained(checkpoint, truncation_side='right', trust_remote_code=True)
tokenizer.padding_side = "right"
if tokenizer.pad_token is None:
  tokenizer.pad_token = tokenizer.bos_token if tokenizer.bos_token is not None else tokenizer.eos_token

# for multiple GPUs install accelerate and do `model = AutoModelForCausalLM.from_pretrained(checkpoint, device_map="auto")`
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint, resume_download=True).to(device)
# translator = Translator()
pygame.mixer.init()

def speech():
    mic = speech_recog.Microphone()
    recog = speech_recog.Recognizer()

    with mic as audio_file:

        recog.adjust_for_ambient_noise(audio_file)
        audio = recog.listen(audio_file)

    try:
        text = recog.recognize_google(audio, language="id-ID")
        print(f">> User (speech): {text}")
        return text
    except speech_recog.UnknownValueError:
        print("Maaf, saya tidak mengerti apa yang Anda katakan.")
        return None
    except speech_recog.RequestError:
        print("Maaf, layanan pengenalan suara tidak tersedia saat ini.")
        return None

# def speak_text(text, lang='id'):
#     tts = gTTS(text=text, lang=lang)
#     tts.save("response.mp3")
#     playsound("response.mp3")
#     os.remove("response.mp3")

def speak_text(text, lang='id'):
    tts = gTTS(text=text, lang=lang)
    filename = "response.mp3"
    tts.save(filename)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    time.sleep(0.1)  # Small delay to ensure the file is not in use
    os.remove(filename)

def chat():
    messages = []

    # User input method choice
    input_method = input("Pilih metode input (1: Teks, 2: Suara): ")
    
    if input_method == "1":
        use_speech = False
    elif input_method == "2":
        use_speech = True
        print("Silakan berbicara...")
    else:
        print("Pilihan tidak valid. Menggunakan teks sebagai metode input.")
        use_speech = False

    while True:

        if use_speech:
            time.sleep(2)
            user_input = speech()
            if user_input is None:
                continue
        else:
            user_input = input(">> User: ")

        # translate prosess
        # user_input = translator.translate(user_input, src="id", dest="en").text

        if user_input.lower() in ["exit", "quit"]:
            print("Ending the conversation.")
            break
        # prompt = "Answer this question in a simple and relaxed manner, as if you were speaking directly. Avoid answers that are too technical or formal"
        # messages.append({"role": "user", "content": user_input})
        
        # Prepare the prompt
        # prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(user_input, return_tensors="pt", padding=True, truncation=True, max_length=1024).to(device)
        input_size = inputs["input_ids"].shape[1]
        
        # Generate response
        outputs = model.generate(**inputs, min_length=1, max_length=100, no_repeat_ngram_size=2, 
                           top_k=50, top_p=0.92, temperature=0.6, do_sample=True)

        preds = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        # assistant_response = tokenizer.decode(tokens, skip_special_tokens=True)

        # messages.append({"role": "assistant", "content": assistant_response})

        # translated_response = translator.translate(assistant_response, src='en', dest='id').text
        if use_speech:
            speak_text(preds[0])
            print(f">> Assistant: {preds[0]}")
        else:
            print(f">> Assistant: {preds[0]}")
        

if __name__ == "__main__":
    chat()
    # chat_with_ai()
