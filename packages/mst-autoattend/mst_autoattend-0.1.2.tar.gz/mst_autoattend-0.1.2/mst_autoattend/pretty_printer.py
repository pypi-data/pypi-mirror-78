from datetime import datetime
from os import environ
import pathlib

SUPPORTED_TYPES = ["DEBUG", "INFO", "ERROR", "WARNING"]
PATH_TO_HELP = pathlib.Path(__file__).parents[0] / 'static/help.txt'

def print_msg(msg, type):
    if type not in SUPPORTED_TYPES:
        raise Exception("Unsupported type of message")
    if type == "DEBUG" and not environ.get("DEBUG"):
        return
    print('{date} | {type} : {msg}'.format(
        type=type,
        date=datetime.now(),
        msg=msg
        )
    )

def print_help():
    print("""
mst_autoattend is designed to help you attend classes and sleep well as well!

On the first run the program asks the user for the basic information which is stored in your computer and used in subsequent runs.

mst_autoattend supports the following arguments:

--help - show help
--reset - reset configuration

Please report bugs and request features at https://github.com/thealphadollar/mst_autoattend

""")