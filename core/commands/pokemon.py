import discord
from discord.ext import commands
import requests
from core import config

PREFIX = config.PREFIX

class PokeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="pokemon", aliases=["poke"])
    async def pokemon(self, ctx, name: str):
        # Buscar pokemon por el nombre
        url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            pokemon_name = data["name"].capitalize()
            pokemon_id = data["id"]
            pokemon_types = ", ".join([t["type"]["name"] for t in data["types"]])
            pokemon_weight = data["weight"] / 10  # El peso está en hectogramos (decimales)
            pokemon_height = data["height"] / 10  
            pokemon_stats = {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]}
            pokemon_image = data["sprites"]["front_default"]

            # Crear el embed con toda la información
            embed = discord.Embed(
                title=f"Información de {pokemon_name}",
                description=f"ID: {pokemon_id}\nTipos: {pokemon_types}",
                color=discord.Color.green()
            )
            embed.add_field(name="Peso", value=f"{pokemon_weight} kg", inline=True)
            embed.add_field(name="Altura", value=f"{pokemon_height} m", inline=True)
            embed.add_field(name="HP", value=pokemon_stats["hp"], inline=True)
            embed.add_field(name="Ataque", value=pokemon_stats["attack"], inline=True)
            embed.add_field(name="Defensa", value=pokemon_stats["defense"], inline=True)
            embed.add_field(name="Ataque-Especial", value=pokemon_stats["special-attack"], inline=True)
            embed.add_field(name="Defensa-Especial", value=pokemon_stats["special-defense"], inline=True)
            embed.add_field(name="Velocidad", value=pokemon_stats["speed"], inline=True)
            embed.set_thumbnail(url=pokemon_image)

            # Enviar el embed
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se encontró el Pokémon.")
            
async def setup(bot):
    await bot.add_cog(PokeCommands(bot))
