import youtube_dl

# Extract audio from playlist, with auto-numbering
ydl_opts = {
    'cachedir': False,
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    # "outtmpl": "%(playlist_index)s - %(title)s.%(ext)s"
    "outtmpl": "%(title)s.%(ext)s"
}

# Download video with subtitle
# ydl_opts = {
#     "writesubtitles": True,
#     # "skip_download": True,
# }
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([
        "https://www.youtube.com/watch?v=jd1r3n4HKOo",
        "https://www.youtube.com/watch?v=UyfTDbc57E0",
        "https://www.youtube.com/watch?v=Pm4ZUFhWLB4",
        "https://www.youtube.com/watch?v=RFt8RnScxlc",
        "https://www.youtube.com/watch?v=iW7b8Mo_SFU",
    ])
