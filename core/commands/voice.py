import discord
from discord.ext import commands

class VoiceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="join", aliases=["connect", "summon", "j", "metase"])
    async def join(self, ctx):
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
            self.song_queue.clear()
            await ctx.send("Me desconecté del canal de voz 👋")
        else:
            await ctx.send("No estoy en ningún canal de voz 😢")

async def setup(bot):
    await bot.add_cog(VoiceCommands(bot))