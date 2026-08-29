import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import os
from dotenv import load_dotenv
from typing import Final
from collections import deque

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Bot ayarları
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="&", intents=intents)

# youtube-dl ayarları
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# Şarkı kuyruğu (queue) sistemi
music_queue = deque()

# YouTube URL veya arama sonucu işleyen fonksiyon
def get_ytdl_source(query):
    try:
        info = ytdl.extract_info(query, download=False)
        print(info)
        
        if 'url' in info:
            return info['url'], info.get('title', 'Müzik')
        elif 'entries' in info and len(info['entries']) > 0:
            first_entry = info['entries'][0]
            return first_entry['url'], first_entry.get('title', 'Müzik')
        else:
            raise ValueError("URL bulunamadı.")
    except Exception as e:
        print(f"Hata: {e}")
        raise

# Şarkıyı oynatma fonksiyonu
async def play_music(ctx):
    if len(music_queue) > 0:
        source_url, title = music_queue.popleft()
        voice_client = ctx.voice_client

        if not voice_client.is_playing():
            voice_client.play(
                discord.FFmpegPCMAudio(source_url),
                after=lambda e: bot.loop.create_task(play_music(ctx))  # Şarkı bitince sıradakini çal
            )
            await ctx.send(f"Çalıyor: {title}")
        else:
            await ctx.send("Bir hata oluştu: Oynatıcı meşgul.")
    else:
        await ctx.send("Kuyruk boş, başka şarkı ekleyin.")

# Şarkı oynatma komutu
@bot.command()
async def p(ctx, *, search: str):
    if not ctx.author.voice:
        await ctx.send("Bir ses kanalında olman gerekiyor!")
        return

    voice_channel = ctx.author.voice.channel

    if ctx.voice_client is None:
        await voice_channel.connect()

    try:
        source_url, title = get_ytdl_source(search)
        music_queue.append((source_url, title))
        await ctx.send(f"Kuyruğa eklendi: {title}")

        # Eğer oynatıcı çalışmıyorsa sıradaki şarkıyı çal
        if not ctx.voice_client.is_playing():
            await play_music(ctx)
    except Exception as e:
        await ctx.send(f"Bir hata oluştu: {e}")

# Sıradaki şarkıya geçme komutu
@bot.command(aliases=["n"])
async def next(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()  # Mevcut şarkıyı durdur
        await ctx.send("Sıradaki şarkıya geçiliyor...")
    else:
        await ctx.send("Çalan bir şarkı yok.")
    await play_music(ctx)

# Ses kanalından çıkma komutu
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Ses kanalından çıkıldı.")
    else:
        await ctx.send("Bot bir ses kanalında değil.")

# Bot hazır olduğunda çalışan olay
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="DJ Halit 🎧"))
    print(f"DJ Halit başarıyla giriş yaptı: {bot.user}")

# Botu başlat
if __name__ == "__main__":
    bot.run(TOKEN)
