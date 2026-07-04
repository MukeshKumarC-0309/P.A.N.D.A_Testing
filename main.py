"""
P.A.N.D.A - Personalized Automated Next-gen Digital Assistant
Entry point: command loop and routing.

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

run = True

wishme()
while run:
    query_initial = takecommand()
    query = query_initial.lower()

    if 'quit' in query:
        run = False
        break

    elif 'time' in query:
        ti()

    elif 'date' in query:
        date()

    elif 'battery' in query:
        battery()

    elif 'jokes' in query or 'joke' in query:
        joke()

    elif 'wikipedia' in query or 'wiki' in query:
        print('P.A.N.D.A : Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences=2)
            print("P.A.N.D.A : According to Wikipedia : ")
            print(results)
        except wikipedia.exceptions.DisambiguationError:
            print(f"P.A.N.D.A : There are multiple meanings for '{query}'. Please be more specific.")
        except wikipedia.exceptions.PageError:
            print(f"P.A.N.D.A : '{query}' does not match any Wikipedia page. Please try again.")

    elif 'remember' in query or 'rmr' in query:
        remember()

    elif 'youtube' in query:
        import webbrowser as wb
        wb.open("https://www.youtube.com/")

    elif 'google' in query:
        import webbrowser as wb
        wb.open("https://www.google.com/")

    elif "weather" in query:
        print("P.A.N.D.A : What is the city name ? ")
        city_name = takecommand()
        weather(city_name)

    elif 'news' in query:
        News()

    elif 'help' in query:
        help()

    elif 'calculate' in query or 'calculator' in query:
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

    elif 'set' in query:
        password()

    elif 'stopwatch' in query or 'watch' in query:
        stopwatch()

    elif 'countdown' in query:
        sec = int(input("P.A.N.D.A : How many seconds ? "))
        countdown(sec)

    elif 'speed' in query or 'type' in query:
        typing_speed_test()

    elif 'vault' in query:  # SQL CONNECT
        n = 0
        try:
            while n < 3:
                p = input("P.A.N.D.A : Enter your password - ")
                if check_password(p):
                    print("-" * 100)
                    print('PANDA VAULT')
                    print('-' * 100)
                    DATABASE()
                    break
                else:
                    print("P.A.N.D.A : Incorrect Password.")
                    print("P.A.N.D.A : Try Again")
                    n += 1
                    if n >= 3:
                        print("P.A.N.D.A : ACCESS DENIED")
                        print("P.A.N.D.A : You do not have access to the database system.")
        except FileNotFoundError:
            print("P.A.N.D.A : Password hasn't been set yet.")
            print('P.A.N.D.A : Please set the password now.')
            password()
            while n < 3:
                p = input("P.A.N.D.A : Enter your password - ")
                if check_password(p):
                    print("-" * 100)
                    print('PANDA VAULT')
                    print('-' * 100)
                    DATABASE()
                    break
                else:
                    print("P.A.N.D.A : Incorrect Password.")
                    print("P.A.N.D.A : Try Again.")
                    n += 1
                    if n >= 3:
                        print("P.A.N.D.A : ACCESS DENIED")
                        print("P.A.N.D.A : You don't have access to the database system")

    elif 'change' in query:
        p = input("P.A.N.D.A : Enter current password - ")
        if check_password(p):
            print('P.A.N.D.A : You can change your password now. ')
            password()
            print("P.A.N.D.A : Password updated succesfully.")
        else:
            print("P.A.N.D.A : Error, invalid input.")

    else:
        print("P.A.N.D.A : I am sorry, I am unable to find a response for this within my servers, redirecting you to Google...")
        open_google_search(query)
