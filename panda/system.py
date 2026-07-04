"""
Core system functions: help text, greeting, command input, date/time/battery.
"""
import datetime
import psutil


def help():
    print('-' * 100)
    print('WELCOME TO THE HELPDESK')
    print("\n This guide will help you traverse through P.A.N.D.A's ecosystem easily and make the best out of its capabilities.\
    \n Use the below listed commands/keywords to access P.A.N.D.A's wide ranging functions.")
    print('-' * 100)
    print('COMMANDS AND KEYWORDS')
    print('-' * 10)
    print(" Date - Displays the date\
    \n Time - Displays the time\
    \n Battery - Displays the current battery status \
    \n Joke - Shares a joke from P.A.N.D.A's expansive archive of hilarious one-line\
    \n Calculator - P.A.N.D.A's in-built calculator helps with basic mathematical calculations\
    \n News - P.A.N.D.A presents you with the latest in new \
    \n Wikipedia - P.A.N.D.A summarises all your queries  \
    \n Remember - P.A.N.D.A stores you memos for you \
    \n Weather - P.A.N.D.A gives you a comprehensive weather report \
    \n Password - P.A.N.D.A saves or changes ( enter CHANGE ) your password to access the databases \
    \n Stopwatch - P.A.N.D.A becomes your pocket stopwatch to track time \
    \n Countdown - P.A.N.D.A commences a countdown timer \
    \n P.A.N.D.A Search - Redirects your out-of-the-box queries to Google ")
    print('-' * 100)


def wishme():
    print("P.A.N.D.A : Welcome back ")
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        print("P.A.N.D.A : Good morning")
    elif hour >= 12 and hour < 18:
        print("P.A.N.D.A : Good afternoon ")
    elif hour >= 18 and hour < 24:
        print("P.A.N.D.A : Good evening ")
    else:
        print("P.A.N.D.A : Good night ")
    print("P.A.N.D.A : PANDA at your service...")
    print('( Type HELP for Commands and QUIT to SHUTDOWN ) ')


def takecommand():
    tc = input('YOU : ')
    return tc


def date():
    year = (datetime.datetime.now().year)
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    print('P.A.N.D.A : ', day, '/', month, '/', year)


def ti():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    print('P.A.N.D.A : ', Time)


def battery():
    battery = psutil.sensors_battery()
    print("P.A.N.D.A : Battery is at", battery.percent, '%')
