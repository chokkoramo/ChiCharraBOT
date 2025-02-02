import discord
from discord.ext import commands
import os
from words import random_word
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = "!"  # Corregido el nombre de la variable

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Para leer mensajes
intents.reactions = True  # Para agregar reacciones
intents.voice_states = True  # Para unirse a canales de voz
intents.guilds = True  # Para acceder a la información del servidor
intents.members = True  # Para obtener información de los miembros

# Creación del bot
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    print(f'Prefijo cargado como {PREFIX}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'pocillo' in message.content.lower():
        await message.add_reaction('🦟')
        await message.reply(random_word(), mention_author=True)

    if 'hola' in message.content.lower():
        await message.channel.send(file=discord.File('img/alpargatas.png'))

    if 'pirinola' in message.content.lower():
        await message.channel.send(file=discord.File('img/icetex.png'))

    # Procesar los comandos
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send("¡Pong!")

@bot.command()
async def join(ctx):
    """El bot se une al canal de voz del usuario"""
    member = ctx.guild.get_member(ctx.author.id)  # Obtener explícitamente el miembro del servidor
    if member and member.voice:  # Verifica si el miembro está en un canal de voz
        channel = member.voice.channel
        try:
            await channel.connect()
            await ctx.send(f"Me uní a {channel.name} 🔊")
        except Exception as e:
            await ctx.send(f'Error al unirse al canal de voz: {e}')
    else:
        await ctx.send("No estás en un canal de voz o no te encontré 😢")

@bot.command()
async def leave(ctx):
    """El bot sale del canal de voz"""
    if ctx.voice_client:  # Verifica si el bot está en un canal de voz
        await ctx.voice_client.disconnect()
        await ctx.send("Me desconecté del canal de voz 👋")
    else:
        await ctx.send("No estoy en ningún canal de voz 😢")

@bot.command()
async def play(ctx):
    """El bot reproduce un archivo de audio"""
    if ctx.voice_client:
        ffmpeg_path = "C:/Users/JUAN CAMILO/Desktop/ffmpeg-2025-01-30-git-1911a6ec26-essentials_build/ffmpeg-2025-01-30-git-1911a6ec26-essentials_build/bin/ffmpeg.exe"
        source = discord.FFmpegPCMAudio("data/audio.mp3", executable=ffmpeg_path)  # Asegúrate de que el archivo existe
        try:
            ctx.voice_client.play(source)
            await ctx.send("🎵 Reproduciendo audio...")
        except Exception as e:
            await ctx.send(f'Error al reproducir el audio: {e}')
    else:
        await ctx.send("No estoy en un canal de voz. Usa `<join` primero.")

# Ejecutar el bot
bot.run(TOKEN)
