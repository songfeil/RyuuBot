import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from commands.test import TestCog
from commands.voice_control import VoiceControlCog
from commands.tts import TtsCog
from commands.youtube import YoutubeCog

os.makedirs("tmp", exist_ok=True)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot 加载Cog中...')
    await bot.add_cog(TestCog(bot))
    await bot.add_cog(VoiceControlCog(bot))
    await bot.add_cog(TtsCog(bot))
    await bot.add_cog(YoutubeCog(bot))
    print(f'Bot 已登录为 {bot.user}')

load_dotenv()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
