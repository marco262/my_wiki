from argparse import ArgumentParser
from time import sleep

from src.server import Server

parser = ArgumentParser()
parser.add_argument('-d', '--debug', action="store_true")
parser.add_argument('-w', '--disable-watchdog', action="store_true")
args = parser.parse_args()

ENABLE_WATCHDOG = not args.disable_watchdog

while True:
    try:
        Server(debug=args.debug)
    except KeyboardInterrupt:
        if not ENABLE_WATCHDOG:
            break
    sleep(10)
