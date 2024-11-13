import discord
from discord.ext import commands
import os
import yt_dlp

from commands.utils.audio_task_queue import audio_task_queue
from commands.utils.youtube_audio_task import YoutubeAudioTask

class YoutubeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.yt_dl_options = {
            "format": "bestaudio/best",
            "extract_flat": True,
            "quiet": False
        }
        self.ytdl = yt_dlp.YoutubeDL(self.yt_dl_options)

    @commands.command()
    async def youtube(self, ctx, url):
        info = self.ytdl.extract_info(url, download=False)
        
        if "entries" in info:
            await ctx.send("检测到播放列表！")
            for entry in info["entries"]:
                await audio_task_queue.enqueue(ctx.guild.id, YoutubeAudioTask(entry["url"]))
                await ctx.invoke(self.bot.get_command("play_queue"))
        else:
            await audio_task_queue.enqueue(ctx.guild.id, YoutubeAudioTask(url))
            await ctx.invoke(self.bot.get_command("play_queue"))

    def clean_up(self, file_path):
        """播放结束后删除本地文件"""
        if os.path.exists(file_path):
            os.remove(file_path)

    def get_volume(self):
        return 0.25

def setup(bot):
    bot.add_cog(MyCog(bot))