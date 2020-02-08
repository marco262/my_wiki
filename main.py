from argparse import ArgumentParser

from src.server import Server

parser = ArgumentParser()
parser.add_argument('-d', '--debug', action="store_true")
args = parser.parse_args()

Server(debug=args.debug)
