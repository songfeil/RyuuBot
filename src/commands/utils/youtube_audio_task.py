from gtts import gTTS
import os
import yt_dlp


class YoutubeAudioTask(object):
    yt_dl_options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'keepvideo': False,
        "outtmpl": "tmp/%(title)s.%(ext)s",
        "noplaylist": True,
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

    def get_volume(self):
        return 0.25

    def __str__(self):
        return "（Youtube）" + self.url
