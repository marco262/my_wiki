import youtube_dl

# Extract audio from playlist, with auto-numbering
# ydl_opts = {
#     'cachedir': False,
#     'format': 'bestaudio/best',
#     'postprocessors': [{
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'mp3',
#         'preferredquality': '192',
#     }],
#     # "outtmpl": "%(playlist_index)s - %(title)s.%(ext)s"
#     "outtmpl": "%(title)s.%(ext)s"
# }

# Download video with subtitle
ydl_opts = {
    # "writesubtitles": True,
    # "skip_download": True,
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([
        "https://www.youtube.com/watch?v=SH_oC5j85Xk",
        "https://www.youtube.com/watch?v=kcOtt7aosJg",
        "https://www.youtube.com/watch?v=rpfhRUsUlq4",
        "https://www.youtube.com/watch?v=Ogka7x5NJbg",
        "https://www.youtube.com/watch?v=5SV-PiVxHM8",
        "https://www.youtube.com/watch?v=62TdOYRKDqc",
        "https://www.youtube.com/watch?v=B-F7XgvgoOI",
        "https://www.youtube.com/watch?v=XPD_xp_Z_nQ",
        "https://www.youtube.com/watch?v=3bDzGUjpkwA",
        "https://www.youtube.com/watch?v=w1ygoNlN66g",
        "https://www.youtube.com/watch?v=l1Kjpq3FUOE",
        "https://www.youtube.com/watch?v=l8wD6TIQK8Y",
        "https://www.youtube.com/watch?v=GlPPysdcWtQ",
        "https://www.youtube.com/watch?v=Ogka7x5NJbg",
        "https://www.youtube.com/watch?v=HhO570NLIWA",
        "https://www.youtube.com/watch?v=O2_ki-NX8_Y",
    ])
