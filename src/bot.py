import discord
from discord.ext import commands
import yt_dlp
from gtts import gTTS
from dotenv import load_dotenv
import os
import uuid

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

os.makedirs("tmp", exist_ok=True)

# 设置 yt-dlp 的选项，确保获取最佳音频流
yt_dl_options = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'noplaylist': True,
    'keepvideo': False,
    "outtmpl": "tmp/%(title)s.%(ext)s",
    'quiet': True
}
ytdl = yt_dlp.YoutubeDL(yt_dl_options)

@bot.event
async def on_ready():
    print(f'Bot 已登录为 {bot.user}')

@bot.command(name="join")
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        await ctx.send("已加入语音频道!")
    else:
        await ctx.send("你需要先进入一个语音频道！")

@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("已离开语音频道!")
    else:
        await ctx.send("Bot 当前不在任何语音频道中。")

@bot.command(name="play")
async def play(ctx, url):
    if not ctx.voice_client:
        await join(ctx)
    if ctx.voice_client:
        try:
            info = ytdl.extract_info(url, download=True)
            file_path = ytdl.prepare_filename(info)
            source = discord.FFmpegOpusAudio(file_path)
            ctx.voice_client.play(source, after=lambda e: clean_up(file_path))
            await ctx.send(f"正在播放: {info['title']}")
        except Exception as e:
            await ctx.send("播放出错了！")
            print(e)
    else:
        await ctx.send("Bot没有连接到语音频道，请先使用`!join`命令。")

@bot.command(name="speak")
async def speak(ctx, text):
    if not ctx.voice_client:
        await join(ctx)
    if ctx.voice_client:
        # 生成语音文件
        tts = gTTS(text=text, lang="zh")
        tmp_voice_path = "./tmp/tts_" + str(uuid.uuid4())
        tts.save(tmp_voice_path)

        # 播放语音文件
        ctx.voice_client.play(discord.FFmpegOpusAudio(tmp_voice_path), after=lambda e: clean_up(tmp_voice_path))
        await ctx.send("播放语音中...")
    else:
        await ctx.send("Bot没有连接到语音频道，请先使用`!join`命令。")

def clean_up(file_path):
    """播放结束后删除本地文件"""
    if os.path.exists(file_path):
        os.remove(file_path)

@bot.command(name="pause")
async def pause(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("已暂停播放。")
    else:
        await ctx.send("没有正在播放的音频。")

@bot.command(name="resume")
async def resume(ctx):
    if ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("已恢复播放。")
    else:
        await ctx.send("没有暂停的音频。")

@bot.command(name="stop")
async def stop(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("已停止播放。")
    else:
        await ctx.send("没有正在播放的音频。")

load_dotenv()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))