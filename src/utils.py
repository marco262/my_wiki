import logging
import os
import re
import sys
from configparser import RawConfigParser
from copy import deepcopy
from enum import Enum
from html import unescape
from html.parser import HTMLParser
from logging.handlers import TimedRotatingFileHandler
from os.path import isfile
from shutil import copyfile
from typing import Optional, Union, List

from bottle import template, HTTPError


class Mode(Enum):
    TITLE = "TITLE"
    BRIEF = "BRIEF"
    FULL = "FULL"


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


def setup_logging(name, log_level=None, capture_stderr=True):
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
        dist_config_path = os.path.join(os.path.dirname(__file__), 'config.ini.dist')
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


def results_mode(d: dict, mode: Optional[str]) -> Union[str, dict]:
    """
    Takes in a spell dictionary (or other dict from a TOML file) and returns the contents based on the mode
    passed in. TITLE returns only the title. BRIEF returns everything but the description. FULL returns the full dict.
    :param d: dictionary of data
    :param mode: TITLE (or None), BRIEF, or FULL
    :return:
    """
    if mode is None:
        mode = Mode.TITLE
    if mode == Mode.TITLE.value:
        return d["title"]
    if mode == Mode.BRIEF.value:
        filter_keys = ["description", "at_higher_levels", "description_md"]
        filtered_dict = {}
        for k, v in d.items():
            if k not in filter_keys:
                filtered_dict[k] = v
        return filtered_dict
    if mode == Mode.FULL.value:
        return d
    raise ValueError(f"{mode} is not a valid results mode")


def ordinal(num: str):
    if not num.isdigit():
        return num.title()
    suffix = {"1": "st", "2": "nd", "3": "rd"}
    return num + suffix.get(num, "th") + " Level"


def str_to_bool(s):
    return s and str(s).lower()[0] in ["t", "1", "y"]


def class_spell(spell: dict, classes: List[str], ua_spells: bool) -> bool:
    """
    Helper function for determining if a spell belongs to any of a list of classes
    :param spell: The parsed spell dictionary, containing classes and classes_ua fields
    :param classes: The list of classes to check against
    :param ua_spells: Whether or not to include the classes_ua field in the spell
    :return:
    """
    if set(classes).intersection(spell["classes"]):
        return True
    if ua_spells and set(classes).intersection(spell.get("classes_ua", [])):
        return True
    return False


def create_tooltip(text, tooltip_text=None):
    if tooltip_text is not None:
        return '''
        <div class="tooltip">{}
            <span class="tooltiptext">{}</span>
        </div>'''.format(text, tooltip_text)
    return text


def md_page(page_name, namespace, md_obj):
    formatted_name = re.sub("\W", "-", page_name.lower())
    if isfile(f"views/{namespace}/{formatted_name}.tpl"):
        text = unescape(template(f"views/{namespace}/{formatted_name}.tpl"))
    elif isfile(f"data/{namespace}/{formatted_name}.md"):
        with open(f"data/{namespace}/{formatted_name}.md") as f:
            text = f.read()
    else:
        raise HTTPError(404, f"I couldn't find \"{page_name}\".")
    md = md_obj.parse_md(text)
    return {"title": page_name.title(), "text": md, "toc": md.toc_html}
