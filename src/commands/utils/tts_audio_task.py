from gtts import gTTS
import uuid
import os

class TtsAudioTask(object):
    def __init__(self, text):
        self.text = text
        self.tmp_file_path = "./tmp/tts_" + str(uuid.uuid4())

    def resolve(self):
        # 生成语音文件
        tts = gTTS(text=self.text, lang="zh")
        tts.save(self.tmp_file_path)
        return self.tmp_file_path

    def cleanup(self):
        if os.path.exists(self.tmp_file_path):
            os.remove(self.tmp_file_path)

    def __str__(self):
        return "（语音）" + self.text
    
    def get_volume(self):
        return 1.0