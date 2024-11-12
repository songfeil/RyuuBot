import discord
from discord.ext import commands
import os

from commands.utils.audio_task_queue import audio_task_queue
from commands.utils.youtube_audio_task import YoutubeAudioTask

class YoutubeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def youtube(self, ctx, url):
        await audio_task_queue.enqueue(ctx.guild.id, YoutubeAudioTask(url))
        await ctx.invoke(self.bot.get_command("play_queue"))

    def clean_up(self, file_path):
        """播放结束后删除本地文件"""
        if os.path.exists(file_path):
            os.remove(file_path)

def setup(bot):
    bot.add_cog(MyCog(bot))