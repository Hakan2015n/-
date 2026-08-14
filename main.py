import os
import time
import random
import sounddevice as sd
from scipy.io import wavfile
import speech_recognition as sr
from googletrans import Translator


FS = 44100  
DURATION = 4  
FILENAME = "voice_input.wav"

translator = Translator()


WORDS_POOL = {
    "1": ["кот", "собака", "дом", "солнце", "вода", "яблоко", "книга", "ручка"],
    "2": ["компьютер", "путешествие", "справедливость", "приключение", "здание", "погода"],
    "3": ["достопримечательность", "вдохновение", "архитектура", "обстоятельство", "впечатление"]
}

#  ASCII ГРАФИКА И ИНТЕРФЕЙС  
def print_logo():
    print("""
    
    
    ===================================================
     __      __    _             _____                                
     \ \    / /   (_)           / ____|                               
      \ \  / /___  _  ___  ___ | |  __  __ _ _ __ ___   ___  _  _  _  
       \ \/ // _ \| |/ __|/ _ \| | |_ |/ _` | '_ ` _ \ / _ \| || || | 
        \  /| (_) | | (__|  __/| |__| | (_| | | | | | |  __/|_||_||_| 
         \/  \___/|_|\___|\___| \_____|\__,_|_| |_| |_|\___|(_)(_)(_) 
                                                                      
    ===================================================
   
     Добро пожаловать в  Voice Game! 
    """)


def record_voice(duration=DURATION, filename=FILENAME):
    print(" Запись пойдет через: 3...", end=" ", flush=True)
    time.sleep(1)
    print("2...", end=" ", flush=True)
    time.sleep(1)
    print("1...", flush=True)
    time.sleep(0.5)
    
    print(" ГОВОРИТЕ СЕЙЧАС...")
    
    recording = sd.rec(int(duration * FS), samplerate=FS, channels=1, dtype='int16')
    sd.wait()  
    print(" Запись завершена. Обработка...")
    
    
    wavfile.write(filename, FS, recording)


def recognize_voice(filename=FILENAME):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
    try:
        
        text = recognizer.recognize_google(audio_data, language="en-US")
        return text.lower().strip()
    except sr.UnknownValueError:
        print(" Робот не смог разобрать слова. Попробуйте говорить четче.")
        return ""
    except sr.RequestError:
        print(" Ошибка сети. Проверьте подключение к интернету.")
        return ""


def check_translation_via_google(ru_word, user_en_word):
    try:
        
        translated = translator.translate(ru_word, src='ru', dest='en')
        correct_en = translated.text.lower().strip()
        return user_en_word == correct_en, correct_en
    except Exception:
        
        return False, ""


def play_game():
    print_logo()
    
    
    print(" Выберите уровень сложности:")
    print("1 — Легкий (простые слова, 3 жизни)")
    print("2 — Средний (длинные слова, 2 жизни)")
    print("3 — Тяжелый (сложные абстрактные понятия, 1 жизнь)")
    
    choice = input("Ваш выбор (1-3): ").strip()
    if choice not in ["1", "2", "3"]:
        print(" Неверный ввод! Автоматически выбран Легкий уровень.")
        choice = "1"
    
    
    lives = 3 if choice == "1" else (2 if choice == "2" else 1)
    words_list = WORDS_POOL[choice]
    random.shuffle(words_list)
    
    score = 0  # Система очков 
    round_num = 1
    
    print(f"\n Игра началась! У вас {lives} . Для победы нужно перевести 5 слов.\n")
    
    for ru_word in words_list[:5]:
        print(f"--- Раунд {round_num} ---")
        print(f"слово на русском:  {ru_word.upper()}  ")
        print("Подумайте, как это будет на английском, и приготовьтесь произнести.")
        
        # Запись и распознавание 
        record_voice()
        user_answer = recognize_voice()
        
        if not user_answer:
            print(" Вы промолчали или микрофон не сработал!")
            lives -= 1
        else:
            print(f" Вы сказали: \"{user_answer}\"")
            
            # Проверка перевода через AI/Googletrans 
            is_ai_correct, ai_translation = check_translation_via_google(ru_word, user_answer)
            
            if is_ai_correct:
                print(" Супер! Google Translate подтвердил ваш точный перевод!")
                score += 15  
                print(f" Правильно! +15 очков. Текущий счет: {score} 🏆")
            elif user_answer in ["cat", "dog", "house", "sun", "water", "apple", "pen", "book", 
                                "computer", "travel", "justice", "adventure", "building", "weather",
                                "sight", "inspiration", "architecture", "circumstance", "impression"]:
                
                print(" Верно! Базовый перевод принят.")
                score += 10
                print(f" Правильно! +10 очков. Текущий счет: {score} ")
            else:
                
                print(f" Неверно! ИИ ожидал перевод: '{ai_translation if ai_translation else 'другой вариант'}'")
                lives -= 1
        
        print(f"Осталось жизней: {lives} \n")
        
     # Логика Game over 
        if lives <= 0:
            print("====================================")
            print(" GAME OVER! У вас закончились жизни. ")
            print(f" Ваш итоговый счет: {score} очков.")
            print("====================================")
            return
            
        round_num += 1
        time.sleep(1)
        
    # Победа
    print("====================================")
    print(" ПОЗДРАВЛЯЕМ! Вы прошли все раунды! ")
    print(f" Итоговый счет: {score} очков. Превосходный результат!")
    print("====================================")

if __name__ == "__main__":
    play_game()
