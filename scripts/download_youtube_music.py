import os

import youtube_dl

os.chdir("../static/audio")

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }]
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([
        "https://www.youtube.com/watch?v=FFQkkFLUL4I",
    ])
