from gtts import gTTS
import os
import yt_dlp


class YoutubeAudioTask(object):
    yt_dl_options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'noplaylist': True,
        'keepvideo': False,
        "outtmpl": "tmp/%(title)s.%(ext)s",
        'quiet': True
    }
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)

    def __init__(self, url):
        self.url = url
        self.tmp_file_path = None

    def resolve(self):
        info = self.ytdl.extract_info(self.url, download=True)
        self.tmp_file_path = self.ytdl.prepare_filename(info)
        return self.tmp_file_path

    def cleanup(self):
        if os.path.exists(self.tmp_file_path):
            os.remove(self.tmp_file_path)

    def __str__(self):
        return "Youtube：" + self.url