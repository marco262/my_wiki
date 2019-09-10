import os

import bottle
import markdown2
import toml
from bottle import get, run, template
from fasteners import process_lock

from utils import setup_logging, load_config

VERSION = (0, 0, 1)
VIEWS_DIR = os.path.join(os.path.dirname(__file__), 'views')
RESOURCES_DIR = os.path.join(os.path.dirname(__file__), 'resources')


class Server:
    """
    On load:
     - Check if any other server instances are running, fail if so.
     - Establish logging to the server.log file. Redirect stderr to this log file, to catch the output thrown
       by the Bottle server.
     - Load the WSGI functions.
     - Start the Bottle server.
    """

    server_thread = None
    interval = None

    def __init__(self, host=None, port=None, log_level=None, run_as_thread=None):
        self._get_process_lock()

        cfg = load_config()
        self.logger = setup_logging("log", log_level=log_level)
        self.md = markdown2.Markdown()

        self._load_wsgi_functions()
        self._init_server(
            host=cfg.get("Settings", "host") if host is None else host,
            port=cfg.getint("Settings", "port") if port is None else port,
            run_as_thread=cfg.getboolean("Settings", "run as thread") if run_as_thread is None else run_as_thread
        )

    @staticmethod
    def _get_process_lock():
        lock = process_lock.InterProcessLock("server.lock")
        if not lock.acquire(blocking=False):
            raise ChildProcessError("Server process is already running")

    def _init_server(self, host=None, port=None, run_as_thread=None):
        if run_as_thread:
            from threading import Thread
            self.server_thread = Thread(name="MyWikiServer", target=self._run_server, args=[host, port],
                                        daemon=True)
            self.server_thread.start()
            print("Server thread started.")
        else:
            self._run_server(host, port)

    @staticmethod
    def _run_server(host, port):
        run(host=host, port=port)
        print("Server instance is ending.")

    def _load_wsgi_functions(self):
        """
        Loads functions into the WSGI
        """
        @get('/')
        @get('/help')
        def index_help():
            with open("data/spell/aid.toml") as f:
                t = toml.loads(f.read())
            return t

        @get('/spell/<name>')
        def spell(name):
            name = name.lower()
            with open(f"data/spell/{name}.toml") as f:
                toml_dict = toml.loads(f.read())
            print(toml_dict)
            return template("spell.tpl", **toml_dict)


if __name__ == "__main__":
    Server()
