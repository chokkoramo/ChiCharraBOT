import discord
from discord.ext import commands

class VoiceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="join", aliases=["connect", "summon", "j", "metase"])
    async def join(self, ctx):
        """El bot se une al canal de voz del usuario."""
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            try:
                await channel.connect()
                await ctx.send(f"Me uní a {channel.name} 🔊")
            except Exception as e:
                await ctx.send(f'Error al unirse al canal de voz: {e}')
        else:
            await ctx.send("No estás en un canal de voz o no te encontré 😢")

    @commands.command(name="leave", aliases=["disconnect"])
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Me desconecté del canal de voz 👋")
        else:
            await ctx.send("No estoy en ningún canal de voz 😢")

    @commands.command(name="play", aliases=["p"])
    async def play(self, ctx):
        if ctx.voice_client:
            ffmpeg_path = "C:/Users/JUAN CAMILO/Desktop/ffmpeg-2025-01-30-git-1911a6ec26-essentials_build/ffmpeg-2025-01-30-git-1911a6ec26-essentials_build/bin/ffmpeg.exe"
            source = discord.FFmpegPCMAudio("assets/sounds/audio.mp3", executable=ffmpeg_path)
            try:
                ctx.voice_client.play(source)
                await ctx.send("🎵 Reproduciendo audio...")
            except Exception as e:
                await ctx.send(f'Error al reproducir el audio: {e}')
        else:
            await ctx.send("No estoy en un canal de voz. Usa `~join` primero.")

async def setup(bot):
    await bot.add_cog(VoiceCommands(bot))