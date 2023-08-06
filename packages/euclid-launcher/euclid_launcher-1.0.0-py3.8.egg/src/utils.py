import os

from termcolor import colored
from appdirs import *


def print_message(message, color):
    print("[" + colored('*', color) + f"] {message}")


def say(message, type="message"):
    if type == "message":
        print_message(message, "blue")
    elif type == "success":
        print_message(message, "green")
    elif type == "error":
        print_message(message, "red")


def get_data_path():
    appname = "euclid"
    appauthor = "BrenoGomes"

    return user_data_dir(appname, appauthor)


def get_command_path():
    return os.path.join(get_data_path(), 'commands.json')
