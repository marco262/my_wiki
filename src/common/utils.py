import glob
import json
import logging
import os
import re
import sys
import threading
import time
from collections import defaultdict
from configparser import RawConfigParser
from html import unescape
from html.parser import HTMLParser
from json import dumps
from logging.handlers import TimedRotatingFileHandler
from operator import itemgetter
from os.path import isfile
from shutil import copyfile

import gevent
from gevent import sleep
from geventwebsocket import WebSocketError

from bottle import template, HTTPError, redirect

player_soundboard_stats_threading_lock = threading.Lock()
player_soundboard_stats_filepath = "player_soundboard_stats.json"


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
    if num == "0":
        return num
    suffix = {"1": "st", "2": "nd", "3": "rd"}
    return num + suffix.get(num, "th")


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
    return re.sub(r"\W+", "-", title.lower().replace("'", "")).strip("-")


def page_name_to_title(page_name):
    """
    Converts a markdown filename (e.g. "beast-master-revamped.md") to a title (e.g. "Beast Master Revamped")
    Not a perfect solution.
    :param page_name:
    :return:
    """
    return better_title(page_name.replace("-", " "))


def md_page(page_title, namespace, directory=None, build_toc=True, markdown_parser=None, load_template=True, **kwargs):
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
    elif load_template:
        if "title" not in kwargs:
            kwargs["title"] = better_title(page_title)
        if build_toc:
            if md.metadata.get("toc") != "false":
                kwargs["toc"] = md.toc_html
        kwargs["text"] = md
        kwargs["accordion_text"] = markdown_parser.accordion_text

        return template("common/page.tpl", kwargs)
    else:
        return md


articles = ["a", "an", "the"]
coordinating_conjunctions = ["and", "but", "for", "nor", "or", "so", "yet"]
prepositions = ["at", "by", "for", "from", "in", "of", "off", "on", "over", "to", "up", "with"]
exceptions = set(articles + coordinating_conjunctions + prepositions)


def better_title(s: str) -> str:
    out_s = []
    for i, word in enumerate(s.split(" ")):
        if i > 0 and word.lower() in exceptions:
            out_s.append(word)
        else:
            out_s.append(word.capitalize())
    return " ".join(out_s)


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


def track_player_soundboard_clicks(params):
    print("player soundboard click", params)
    if params["action"] != "load":
        return
    with player_soundboard_stats_threading_lock:
        file_url = params["url"]
        if os.path.isfile(player_soundboard_stats_filepath):
            with open(player_soundboard_stats_filepath) as f:
                player_soundboard_stats = json.load(f)
        else:
            player_soundboard_stats = {}
        if file_url not in player_soundboard_stats:
            player_soundboard_stats[file_url] = []
        player_soundboard_stats[file_url].append(time.time())
        with open(player_soundboard_stats_filepath, "w") as f:
            json.dump(player_soundboard_stats, f)


def get_player_soundboard_stats():
    last_week_start = time.time() - (7 * 86400)
    last_week_stats = defaultdict(list)
    last_month_start = time.time() - (30 * 86400)
    last_month_stats = defaultdict(list)
    all_time_stats = defaultdict(list)
    with player_soundboard_stats_threading_lock:
        with open(player_soundboard_stats_filepath) as f:
            player_soundboard_stats = json.load(f)
    g = glob.glob("media/audio/requests/*")
    print(os.getcwd())
    print(g)
    for filepath in glob.glob("media/audio/requests/*"):
        print(filepath)
        normalized_filepath = "/" + filepath.replace("\\", "/")
        times_played = player_soundboard_stats.get(normalized_filepath, [])
        last_week = 0
        last_month = 0
        all_time = 0
        for time_played in times_played:
            if time_played > last_week_start:
                last_week += 1
            if time_played > last_month_start:
                last_month += 1
            all_time += 1
        trimmed_filepath = normalized_filepath.replace("/media/audio/", "")
        last_week_stats[last_week].append(trimmed_filepath)
        last_month_stats[last_month].append(trimmed_filepath)
        all_time_stats[all_time].append(trimmed_filepath)
    return {
        "last_week_stats": sorted(last_week_stats.items(), key=itemgetter(0), reverse=True),
        "last_month_stats": sorted(last_month_stats.items(), key=itemgetter(0), reverse=True),
        "all_time_stats": sorted(all_time_stats.items(), key=itemgetter(0), reverse=True),
    }