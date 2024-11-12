import discord
from discord.ext import commands
import os

from commands.utils.audio_task_queue import audio_task_queue
from commands.utils.tts_audio_task import TtsAudioTask

class TtsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def baz(self, ctx, text):
        audio_task_queue.test()
        await ctx.send("baz " + text)

    @commands.command()
    async def speak(self, ctx, text):
        await audio_task_queue.enqueue(ctx.guild.id, TtsAudioTask(text))
        await ctx.invoke(self.bot.get_command("play_queue"))

    def clean_up(self, file_path):
        """播放结束后删除本地文件"""
        if os.path.exists(file_path):
            os.remove(file_path)

def setup(bot):
    bot.add_cog(MyCog(bot))