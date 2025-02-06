import discord
from discord.ext import commands
from core.utils.helpers import random_word

class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if 'pocillo' in message.content.lower():
            await message.add_reaction('🦟')
            await message.reply(random_word(), mention_author=True)

        if 'hola' in message.content.lower() or 'ola' in message.content.lower():
            await message.channel.send(file=discord.File('assets/img/alpargatas.png'))

        if 'pirinola' in message.content.lower():
            await message.channel.send(file=discord.File('assets/img/icetex.png'))
            
        if 'melo' in message.content.lower():
            await message.add_reaction('❤️')
            await message.reply('Con gusto mi amor 😍', mention_author=True)

async def setup(bot):
    await bot.add_cog(FunCommands(bot))