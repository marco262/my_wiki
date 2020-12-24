import logging
import os
import re
import sys
from configparser import RawConfigParser
from html import unescape
from html.parser import HTMLParser
from json import dumps
from logging.handlers import TimedRotatingFileHandler
from os.path import isfile
from shutil import copyfile

import gevent
from bottle import template, HTTPError, redirect
from gevent import sleep
from geventwebsocket import WebSocketError


# Taken from http://www.electricmonk.nl/log/2011/08/14/redirect-stdout-and-stderr-to-a-logger-in-python/
class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())


def setup_logging(name, log_level=None, capture_stderr=False):
    cfg = load_config()
    level = getattr(logging, cfg.get('Logging', 'level') if log_level is None else log_level)
    logs_folder = './logs'
    os.makedirs(logs_folder, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = TimedRotatingFileHandler(os.path.join(logs_folder, name + ".log"), when="midnight")
    formatter = logging.Formatter(cfg.get('Logging', 'format'), cfg.get('Logging', 'date format'))
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if capture_stderr:
        stderr_logger = logging.getLogger('STDERR')
        stderr_logger.addHandler(handler)
        sl = StreamToLogger(stderr_logger, logging.ERROR)
        sys.stderr = sl

    return logger


def load_config():
    # Create config folder
    config_folder = "."
    os.makedirs(config_folder, exist_ok=True)
    # Check for config file. If it doesn't exist, copy it over
    config_path = os.path.join(config_folder, "config.ini")
    if not os.path.isfile(config_path):
        dist_config_path = "config.ini.dist"
        copyfile(dist_config_path, config_path)
    # Load config file and return it
    cfg = RawConfigParser()
    cfg.read(config_path)
    return cfg


def delete_config():
    config_path = "./config.ini"
    os.remove(config_path)
    print(config_path, "has been removed.")


# Taken from https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_html(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def ordinal(num: str):
    if not num.isdigit():
        return num.title()
    suffix = {"1": "st", "2": "nd", "3": "rd"}
    return num + suffix.get(num, "th") + " Level"


def str_to_bool(s):
    return s and str(s).lower()[0] in ["t", "1", "y"]


def create_tooltip(text, tooltip_text=None):
    if tooltip_text is not None:
        return '''
        <div class="tooltip">{}
            <span class="tooltiptext">{}</span>
        </div>'''.format(text, tooltip_text)
    return text


def title_to_page_name(title):
    """
    Converts a title (e.g. "Beast Master (Revamped)") to a markdown filename (e.g. "beast-master-revamped")
    :param title:
    :return:
    """
    return re.sub(r"\W+", "-", title.lower()).strip("-")


def page_name_to_title(page_name):
    """
    Converts a markdown filename (e.g. "beast-master-revamped.md") to a title (e.g. "Beast Master Revamped")
    Not a perfect solution.
    :param page_name:
    :return:
    """
    return page_name.replace("-", " ").title()


def md_page(page_title, namespace, directory=None, build_toc=True, markdown_parser=None, **kwargs):
    if markdown_parser is None:
        # Avoiding circular dependencies
        from src.common.markdown_parser import DEFAULT_MARKDOWN_PARSER
        markdown_parser = DEFAULT_MARKDOWN_PARSER
    path_name = title_to_page_name(page_title)
    if directory:
        path_name = os.path.join(directory, path_name)
    if namespace:
        path_name = os.path.join(namespace, path_name)
    template_path = f"views/{path_name}.tpl"
    md_path = f"data/{path_name}.md"

    if isfile(template_path):
        text = unescape(template(template_path, **kwargs))
    elif isfile(md_path):
        with open(md_path, encoding="utf-8") as f:
            text = f.read()
    else:
        raise HTTPError(404, f"I couldn't find \"{path_name}\".")
    try:
        md = markdown_parser.parse_md(text, namespace)
    except NameError:
        print(f"Error when converting {path_name}")
        raise
    if md.startswith("<p>REDIRECT "):
        redirect(md[12:-5])
    else:
        if "title" not in kwargs:
            kwargs["title"] = page_title.title()
        if build_toc and not md.startswith("<!-- no-toc -->"):
            kwargs["toc"] = md.toc_html
        kwargs["text"] = md
        kwargs["accordion_text"] = markdown_parser.accordion_text

        return template("common/page.tpl", kwargs)


def websocket_loop(ws, websocket_list):
    print("Opening Websocket {}".format(ws), flush=True)
    websocket_list.append(ws)
    try:
        while True:
            sleep(60)
            # Checking if websocket has been closed by the client
            with gevent.Timeout(1.0, False):
                ws.receive()
            if ws.closed:
                print("WebSocket was closed by the client: {}".format(ws), flush=True)
                break
    except Exception as e:
        print("Error in WebSocket loop: {}".format(e), flush=True)
    finally:
        if not ws.closed:
            print("Closing WebSocket: {}".format(ws), flush=True)
            ws.close()
        try:
            websocket_list.remove(ws)
        except ValueError as e:
            print(e, ws)


def send_to_websockets(payload, websocket_list):
    print(websocket_list, flush=True)
    for ws in websocket_list[:]:
        try:
            print(f"Sending payload {payload} to {ws}", flush=True)
            ws.send(dumps(payload))
        except WebSocketError:
            print(f"Failed to send message to {ws}. Removing from list", flush=True)
            websocket_list.remove(ws)
        except Exception as e:
            print(f"Error when sending message to {ws}. {e}", flush=True)
            websocket_list.remove(ws)
