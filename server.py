# Python standard libraries
import os
from json import dumps

# Library modules
import markdown2

from utils import setup_logging, load_config

# 3rd party modules
from fasteners import process_lock
from bottle import get, run

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
        global logger

        self._get_process_lock()

        cfg = load_config()
        logger = setup_logging("log", log_level=log_level)
        self.markdowner = markdown2.Markdown()

        self._load_wsgi_functions()
        self._init_server(
            host=cfg.get("Settings", "host") if host is None else host,
            port=cfg.getint("Settings", "port") if port is None else port,
            run_as_thread=cfg.getboolean("Settings", "run as thread") if run_as_thread is None else run_as_thread
        )

    def _get_process_lock(self):
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

    def _run_server(self, host, port):
        run(host=host, port=port)
        print("Server instance is ending.")

    def _load_wsgi_functions(self):
        """
        Loads functions into the WSGI
        """
        @get('/')
        @get('/help')
        def index_help():
            return self.markdowner.convert("*boo!*\n\n**eek!**")


if __name__ == "__main__":
    Server()
