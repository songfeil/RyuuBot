import discord
from discord.ext import commands

from commands.utils.audio_task_queue import audio_task_queue

class VoiceControlCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
            await ctx.send("已加入语音频道!")
        else:
            await ctx.send("你需要先进入一个语音频道！")

    @commands.command()
    async def leave(self, ctx):
        await ctx.invoke(self.bot.get_command("stop"))
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("已离开语音频道!")
        else:
            await ctx.send("Bot 当前不在任何语音频道中。")

    @commands.command()
    async def play_queue(self, ctx):
        if not ctx.voice_client:
            await self.join(ctx)
        if ctx.voice_client and not ctx.voice_client.is_playing():
            await self.clean_and_play_next(ctx)

    async def clean_and_play_next(self, ctx, last_audio_task=None):
        if last_audio_task is not None:
            last_audio_task.cleanup()
        audio_task = await audio_task_queue.dequeue(ctx.guild.id)
        if audio_task is not None:
            audio_volume = audio_task.get_volume()
            volume_control_option = f'-vn -filter:a "volume={audio_volume:.2f}"'
            ctx.voice_client.play(discord.FFmpegOpusAudio(audio_task.resolve(), options=volume_control_option), after=lambda e: self.bot.loop.create_task(self.clean_and_play_next(ctx, last_audio_task=audio_task)))
            await ctx.send("正在播放：" + str(audio_task))

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("已跳过当前歌曲。")
            await self.clean_and_play_next(ctx)

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("已暂停播放。")
        else:
            await ctx.send("没有正在播放的音频。")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("已恢复播放。")
        else:
            await ctx.send("没有暂停的音频。")

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await audio_task_queue.clear(ctx.guild.id)
            await ctx.send("停止播放。")


def setup(bot):
    bot.add_cog(MyCog(bot))