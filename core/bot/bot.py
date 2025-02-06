import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from core import config

PREFIX = config.PREFIX
INTENTS = config.INTENTS

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Crear los intents
intents = discord.Intents.default()
for intent, value in INTENTS.items():
    setattr(intents, intent, value)

# Crear el bot
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Cargar los Cogs
async def load_cogs():
    await bot.load_extension("core.events.on_ready")  
    await bot.load_extension("core.commands.general")  
    await bot.load_extension("core.commands.fun")      
    await bot.load_extension("core.commands.voice")
    await bot.load_extension("core.commands.music_player")
    await bot.load_extension("core.commands.pokemon")    

async def run_bot():
    await load_cogs() 
    await bot.start(TOKEN)  
