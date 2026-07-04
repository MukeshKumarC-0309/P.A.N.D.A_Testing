"""
Everyday utility functions: reminders, jokes, news, weather, calculator,
stopwatch, countdown, typing speed test, and web search.
"""
import time
import random
import requests
import pyjokes
import webbrowser as wb
import urllib.parse

from panda.system import takecommand
from config import WEATHER_API_KEY, NEWS_API_KEY


def remember():
    choice = input("P.A.N.D.A : Do you want to remember something or check your reminders?")
    if "remember" in choice.lower():
        print("P.A.N.D.A : What do you want me to remember ?")
        remember_file = open('rmr.txt', 'w+')
        while True:
            inp = takecommand()
            if 'exit' in inp.lower():
                remember_file.close()
                break
            else:
                print("P.A.N.D.A : Remembering - " + inp)
                remember_file.write(inp + '\n')
    elif "reminder" in choice.lower():
        try:
            print("P.A.N.D.A : Checking your reminders...")
            f = open("rmr.txt", "r")
            for s in f.readlines():
                print(s)
        except FileNotFoundError:
            print("P.A.N.D.A : No reminders have been stored.", end=' ')
            print("Please try again")


def joke():
    print('P.A.N.D.A : ', pyjokes.get_joke())


def News():
    # BBC news via NewsAPI — key now loaded from environment, not hardcoded
    newsq = {
        "source": "bbc-news",
        "sortBy": "top",
        "apiKey": NEWS_API_KEY
    }
    main_url = "https://newsapi.org/v1/articles"

    res = requests.get(main_url, params=newsq)
    open_bbc_page = res.json()

    article = open_bbc_page["articles"]
    results = []

    for ar in article:
        results.append(ar["title"])

    for i in range(len(results)):
        print(i + 1, results[i])


def weather(city_name):
    # Weather via OpenWeatherMap — key now loaded from environment, not hardcoded
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + WEATHER_API_KEY + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        print('P.A.N.D.A : ')
        print(" Temperature in kelvin unit = " +
              str(current_temperature) +
              "\n humidity (in percentage) = " +
              str(current_humidiy) +
              "\n description = " +
              str(weather_description))
    else:
        print("P.A.N.D.A : City not Found")


def add(num1, num2):
    return num1 + num2


def subtract(num1, num2):
    return num1 - num2


def multiply(num1, num2):
    return num1 * num2


def divide(num1, num2):
    return num1 / num2


def stopwatch():
    print("-" * 100, '\n\t\tSTOPWATCH\n', '-' * 100)
    print("Instructions:")
    print("Press 's' to start the stopwatch")
    print("Press 'p' to pause/stop the stopwatch")
    print("Press 'r' to reset the stopwatch")
    print("Press 'q' to quit")

    start_time = 0
    elapsed_time = 0
    running = False

    while True:
        command = input("Enter command: ").strip().lower()

        if command == 's':
            if not running:
                start_time = time.time() - elapsed_time
                running = True
                print("Stopwatch started")
            else:
                print("Stopwatch is already running")

        elif command == 'p':
            if running:
                elapsed_time = time.time() - start_time
                running = False
                print(f"Stopwatch stopped at {elapsed_time:.2f} seconds")
            else:
                print(f"Stopwatch is not running. Elapsed time: {elapsed_time:.2f} seconds")

        elif command == 'r':
            start_time = 0
            elapsed_time = 0
            running = False
            print("Stopwatch reset")

        elif command == 'q':
            if running:
                elapsed_time = time.time() - start_time
            print(f"Quitting. Final time: {elapsed_time:.2f} seconds")
            break

        else:
            print("Unknown command. Please use 's' to start, 'p' to pause, 'r' to reset, 'q' to quit.")
    print()


def countdown(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f'{mins:02d}:{secs:02d}'
        print(timer, end="\r")
        time.sleep(1)
        seconds -= 1
    print("P.A.N.D.A : Time's up!")
    print()


def _choose_sentence():
    sents = [
        "The quick brown fox jumps over the lazy dog.",
        "Cats chase mice around the garden in playful spurts.",
        "Typing fast helps complete tasks with time to spare.",
        "Keyboard warriors compete in speed and skill daily.",
        "The sun sets behind mountains, casting golden rays.",
        "Practice typing regularly to improve your speed score.",
        "Running through the forest, the deer leaped gracefully.",
        "Waves crash against the shore, spraying salty mist.",
        "Typing games make practice fun and engaging.",
        "Bright stars twinkle in the night sky, guiding travelers.",
        "The chef prepared a feast with fresh, local ingredients.",
        "Quick fingers tap the keys, letters forming words.",
        "Focus and accuracy are the keys to typing success.",
        "The wind whispers secrets through the ancient trees.",
        "Lightning flashed, illuminating the dark, stormy night.",
        "The artist painted a vibrant scene of city life."
    ]
    return random.choice(sents)


def typing_speed_test():
    print("-" * 100, '\n\t\tTYPING SPEED TEST\n', '-' * 100)
    test_sentence = _choose_sentence()
    print("Typing Speed Test")
    print("Type the following sentence as fast as you can:")
    print(test_sentence)
    print("\nPress Enter when you're ready to start.")

    input()

    start_time = time.time()
    typed_sentence = input("\nStart typing now: ")
    end_time = time.time()

    elapsed_time = end_time - start_time
    words_typed = len(typed_sentence.split())
    words_per_minute = (words_typed / elapsed_time) * 60

    accuracy = sum(
        1 for i, c in enumerate(test_sentence)
        if i < len(typed_sentence) and c == typed_sentence[i]
    ) / len(test_sentence) * 100

    print(f"\nTime taken: {elapsed_time:.2f} seconds")
    print(f"Words typed: {words_typed}")
    print(f"Words per minute (WPM): {words_per_minute:.2f}")
    print(f"Accuracy: {accuracy:.2f}%")
    print()


def open_google_search(query):
    encoded_query = urllib.parse.quote_plus(query)
    search_url = f"https://www.google.com/search?q={encoded_query}"
    wb.open(search_url)
    print()
