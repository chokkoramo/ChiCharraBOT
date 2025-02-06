import discord
from discord.ext import commands
import yt_dlp

class MusicPlayerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = []
         
    @commands.command(name="play", aliases=["p", "quiero escuchar"])
    async def play(self, ctx, *, query: str):
        vc = ctx.voice_client
        if not vc:
            await self.join(ctx)
            vc = ctx.voice_client

        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "noplaylist": True,
            "extractor_args": {"youtube": {"player_client": ["web"]}}
        }

        if "youtube.com" in query or "youtu.be" in query:
            search_query = query
        else:
            search_query = f"ytsearch:{query}" 

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=False)
            if "entries" in info:
                info = info["entries"][0]

            audio_url = info["url"]
            title = info["title"]

        if vc.is_playing():
            self.song_queue.append((audio_url, title))
            await ctx.send(f"🎵 **{title}** se agregó a la cola.")
        else:
            self.play_song(ctx, audio_url, title)
            
    async def next_song(self, ctx):
        vc = ctx.voice_client
        if self.song_queue:
            next_audio, next_title = self.song_queue.pop(0)
            await ctx.send(f"🎶 Reproduciendo ahora: **{next_title}**")
            vc.play(
                discord.FFmpegPCMAudio(next_audio, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"),
                after=lambda e: self.bot.loop.create_task(self.next_song(ctx))  # 🔥 Ahora maneja la cola correctamente
            )
        else:
            await ctx.send("🎵 No hay más canciones en la cola.")
        
    def play_song(self, ctx, audio_url, title):
        vc = ctx.voice_client

        def after_playing(error):
            if error:
                print(f"Error al reproducir: {error}")
            self.bot.loop.call_soon_threadsafe(self.next_song, ctx)

        vc.play(
            discord.FFmpegPCMAudio(audio_url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"),
            after=after_playing
        )

        self.bot.loop.create_task(ctx.send(f"🎶 Reproduciendo: **{title}**"))
            
    @commands.command(name="pause", aliases=["quieto", "pausar"])
    async def pause(self, ctx):
        vc = ctx.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await ctx.send("⏸️ Canción pausada")
        else:
            await ctx.send("No estoy reproduciendo nada 😢")
            
    @commands.command(name="resume", aliases=["continuar", "siga"])
    async def resume(self, ctx):
        vc = ctx.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await ctx.send("▶️ Canción reanudada")
        else:
            await ctx.send("No estoy reproduciendo nada 😢")
            
    @commands.command(name="stop", aliases=["detener", "parar", "no mas"])
    async def stop(self, ctx):
        vc = ctx.voice_client
        if vc:
            vc.stop()
            self.song_queue.clear()
            await ctx.send("⛔ Música detenida y cola vaciada")
        else:
            await ctx.send("No estoy reproduciendo nada 😢")
                    
    @commands.command(name="skip", aliases=["siguiente", "next"])
    async def skip(self, ctx):
        """Salta la canción actual y reproduce la siguiente."""
        vc = ctx.voice_client
        if vc and vc.is_playing():
            vc.stop()
            await self.next_song(ctx)  # ✅ Ahora llama correctamente a la siguiente canción
            await ctx.send("⏭️ Canción saltada")
        else:
            await ctx.send("😥 No hay música en reproducción.")

async def setup(bot):
    await bot.add_cog(MusicPlayerCommands(bot))