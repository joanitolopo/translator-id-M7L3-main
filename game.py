from speech import speech
from random import choice, randint
import time

# Difficulty levels
levels = {"mudah": ["diary", "friend", "mouse"],
          "sedang": ["computer", "algorithm", "developer"],
          "sulit": ["neural network", "machine learning", "artificial intelligence"]
          }

def play_game(level):
    words = levels.get(level, [])  # Pemilihan kata berdasarkan tingkatan
    if not words:
        print("Salah ketik.")
        return

    score = 0
    num_attempts = 3  # Jumlah percobaan per kata

    for _ in range(len(words)):
        random_word = choice(words)
        print(f"Silakan ucapkan {random_word}")
        recog_word = speech(lang="en-EN")
        print(recog_word)
        
        if random_word == recog_word:
            print("Itu Benar!")
            score += 1
        else:
            print(f"Ada sesuatu yang salah. Kata itu adalah: {random_word}")

        time.sleep(2)  # Tunda beberapa detik
        
    print(f"Game berakhir! Skor kamu adalah: {score}/{len(words)}")

# Select the difficulty level
selected_level = input("Pilih tingkatan game (mudah/sedang/sulit): ").lower()
play_game(selected_level)
