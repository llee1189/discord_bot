import discord
from discord.ext import commands
import DiscordUtils
import os
from googleapiclient.discovery import build

os.environ['API_KEY']
youtube = build('youtube', 'v3', developerKey=os.environ['API_KEY'])

music = DiscordUtils.Music()
bot = commands.Bot(command_prefix='-')


async def play_music(c, u):
    music_player = music.get_player(guild_id=c.guild.id)
    if not music_player:
        music_player = music.create_player(c)
    if not c.voice_client.is_playing():
        await music_player.queue(u, search=True)
        await music_player.play()
    else:
        await music_player.queue(u, search=True)


@bot.event
async def on_ready():
    print('The Bot is ready.')


@bot.command()
async def play(context, url):
    try:
        channel = context.author.voice.channel
        await channel.connect()
    except:
        await play_music(context, url)
    await play_music(context, url)


@bot.command()
async def info(context, url):
    id = url[32:]
    request = youtube.videos().list(
        part="statistics",
        id=id
    )
    response = request.execute()
    views = response.get('items')[0].get('statistics').get('viewCount')
    likes = response.get('items')[0].get('statistics').get('likeCount')
    dislikes = response.get('items')[0].get('statistics').get('dislikeCount')
    comments = response.get('items')[0].get('statistics').get('commentCount')
    await context.send(f"This video has {views} views, {likes} likes, {dislikes} dislikes, and {comments} comments.")


@bot.command()
async def connect(context):
    try:
        channel = context.author.voice.channel
        await channel.connect()
    except:
        await context.send("Already connected!")


@bot.command()
async def leave(context):
    vclient = discord.utils.get(bot.voice_clients, guild=context.guild)
    try:
        await vclient.disconnect()
    except:
        await context.send("The bot is not connected to a voice channel.")


bot.run(os.environ['BOT_KEY'])  # this is my discord bot authentication
