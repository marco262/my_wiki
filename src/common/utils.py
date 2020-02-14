import logging
import os
import re
import sys
from configparser import RawConfigParser
from html import unescape
from html.parser import HTMLParser
from logging.handlers import TimedRotatingFileHandler
from os.path import isfile
from shutil import copyfile

from bottle import template, HTTPError


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


def md_page(page_name, namespace, md_obj, build_toc=True):
    formatted_name = re.sub("\W", "-", page_name.lower())
    template_path = f"views/{namespace}/{formatted_name}.tpl"
    md_path = f"data/{namespace}/{formatted_name}.md"

    if isfile(template_path):
        text = unescape(template(template_path))
    elif isfile(md_path):
        with open(md_path) as f:
            text = f.read()
    else:
        raise HTTPError(404, f"I couldn't find \"{page_name}\".")
    md = md_obj.parse_md(text)
    kwargs = {"title": page_name.title(), "text": md}
    if build_toc:
        kwargs["toc"] = md.toc_html
    return template("common/page.tpl", kwargs)
