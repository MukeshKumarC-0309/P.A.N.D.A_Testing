"""
P.A.N.D.A - Personalized Automated Next-gen Digital Assistant
Entry point: greeting, command loop, and command registration.

Routing is handled by panda/router.py: each command registers keywords
and a handler(query); the loop just dispatches. This replaces the
original if/elif chain and makes it easy to add new capabilities.

Originally developed by Pranav, Mukesh, Vaishanth, and Gautam as a
12th-grade school project. This version removes the games/arcade
module and hardens credential handling and password storage.
"""
import wikipedia

from panda.system import help, wishme, takecommand, date, ti, battery
from panda.auth import password, check_password
from panda.utilities import (
    remember, joke, News, weather, add, subtract, multiply, divide,
    stopwatch, countdown, typing_speed_test, open_google_search
)
from panda.vault import DATABASE
from panda import router, db


# ---------------------------------------------------------------------------
# Command handlers. Each takes the raw query string (some ignore it).
# ---------------------------------------------------------------------------

def handle_wikipedia(query):
    print('P.A.N.D.A : Searching Wikipedia...')
    topic = query.lower().replace("wikipedia", "").replace("wiki", "").strip()
    try:
        results = wikipedia.summary(topic, sentences=2)
        print("P.A.N.D.A : According to Wikipedia : ")
        print(results)
    except wikipedia.exceptions.DisambiguationError:
        print(f"P.A.N.D.A : There are multiple meanings for '{topic}'. Please be more specific.")
    except wikipedia.exceptions.PageError:
        print(f"P.A.N.D.A : '{topic}' does not match any Wikipedia page. Please try again.")


def handle_youtube(query):
    import webbrowser as wb
    wb.open("https://www.youtube.com/")


def handle_google(query):
    import webbrowser as wb
    wb.open("https://www.google.com/")


def handle_weather(query):
    print("P.A.N.D.A : What is the city name ? ")
    city_name = takecommand()
    weather(city_name)


def handle_calculator(query):
    print("Please select operation -\n"
          "1. Add\n"
          "2. Subtract\n"
          "3. Multiply\n"
          "4. Divide\n")
    inp = input('P.A.N.D.A : Enter the Operator - ')
    number_1 = float(input("P.A.N.D.A : Enter first number: "))
    number_2 = float(input("P.A.N.D.A : Enter second number: "))
    if inp.lower() == 'add' or inp.lower() == '+':
        print(number_1, "+", number_2, "=", add(number_1, number_2))
    elif inp.lower() == 'subtract' or inp.lower() == '-':
        print(number_1, "-", number_2, "=", subtract(number_1, number_2))
    elif inp.lower() == 'multiply' or inp.lower() == '*':
        print(number_1, "*", number_2, "=", multiply(number_1, number_2))
    elif inp.lower() == 'divide' or inp.lower() == '/':
        print(number_1, "/", number_2, "=", divide(number_1, number_2))
    else:
        print('P.A.N.D.A : Invalid Input.')


def handle_countdown(query):
    sec = int(input("P.A.N.D.A : How many seconds ? "))
    countdown(sec)


def open_vault():
    """Prompt for the vault password up to 3 times; open it on success.

    Raises FileNotFoundError (from check_password) if no password has
    been set yet, so the caller can prompt the user to set one.
    """
    n = 0
    while n < 3:
        p = input("P.A.N.D.A : Enter your password - ")
        if check_password(p):
            print("-" * 100)
            print('PANDA VAULT')
            print('-' * 100)
            db.unlock(p)          # decrypt the vault into memory
            try:
                DATABASE()
            finally:
                db.lock(p)        # re-encrypt on exit, even if DATABASE() errors
            return
        print("P.A.N.D.A : Incorrect Password.")
        print("P.A.N.D.A : Try Again")
        n += 1
    print("P.A.N.D.A : ACCESS DENIED")
    print("P.A.N.D.A : You do not have access to the database system.")


def handle_vault(query):
    try:
        open_vault()
    except FileNotFoundError:
        print("P.A.N.D.A : Password hasn't been set yet.")
        print('P.A.N.D.A : Please set the password now.')
        password()
        open_vault()


def handle_change(query):
    try:
        p = input("P.A.N.D.A : Enter current password - ")
        if check_password(p):
            print('P.A.N.D.A : You can change your password now. ')
            db.unlock(p)                 # load the vault with the current key
            new_password = password()    # sets the new hash, returns the raw pw
            db.lock(new_password)        # re-encrypt the vault under the new key
            print("P.A.N.D.A : Password updated succesfully.")
        else:
            print("P.A.N.D.A : Error, invalid input.")
    except FileNotFoundError:
        print("P.A.N.D.A : Password hasn't been set yet.")
        print('P.A.N.D.A : Please set the password now.')
        password()


def fallback(query):
    print("P.A.N.D.A : I am sorry, I am unable to find a response for this within my servers, redirecting you to Google...")
    open_google_search(query)


# ---------------------------------------------------------------------------
# Register the built-in commands. Trivial delegations use a small lambda.
# ---------------------------------------------------------------------------

router.register("time", ["time"], lambda q: ti())
router.register("date", ["date"], lambda q: date())
router.register("battery", ["battery"], lambda q: battery())
router.register("joke", ["joke", "jokes"], lambda q: joke())
router.register("wikipedia", ["wikipedia", "wiki"], handle_wikipedia)
router.register("remember", ["remember", "rmr"], lambda q: remember())
router.register("youtube", ["youtube"], handle_youtube)
router.register("google", ["google"], handle_google)
router.register("weather", ["weather"], handle_weather)
router.register("news", ["news"], lambda q: News())
router.register("help", ["help"], lambda q: help())
router.register("calculator", ["calculate", "calculator"], handle_calculator)
router.register("set", ["set"], lambda q: password())
router.register("stopwatch", ["stopwatch", "watch"], lambda q: stopwatch())
router.register("countdown", ["countdown"], handle_countdown)
router.register("typing", ["speed", "type"], lambda q: typing_speed_test())
router.register("vault", ["vault"], handle_vault)
router.register("change", ["change"], handle_change)


def main():
    wishme()
    while True:
        query = takecommand()
        if router.matches("quit", query):
            break
        router.dispatch(query, fallback)


if __name__ == "__main__":
    main()
