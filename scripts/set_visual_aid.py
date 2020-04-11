from tkinter import Tk
from urllib.parse import urlencode

import requests

url = Tk().clipboard_get()

params = urlencode({"url": url})

requests.get("http://mywiki.zapto.org:26262/dragon_heist/set_visual_aid", params=params)