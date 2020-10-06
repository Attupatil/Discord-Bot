import discord
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
import youtube_dl
import random
import pyjokes
from random import choice
import requests

youtube_dl.utils.bug_reports_message = lambda: ''

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
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


client = commands.Bot(command_prefix='sudo ')

status = ['Cool Game', 'ssupp boi', 'Hackerrank', 'GoodGame']

@client.event
async def on_ready():
    change_status.start()
    print('Bot is online!')

@client.event 
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='welcome')
    await channel.send(f'Welcome Welcome Welcome{member.mention}!! `sudo help`')

@client.command(name='ping', help='This command returns the latency')
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: `{round(client.latency * 1000)}ms` ')

@client.command()
async def version(ctx):
    """Check the current bot version"""
    await ctx.send("My current version is `1.3` ")

@client.command(name='ITjoke', help= 'Jokes for IT people')
async def joke(ctx):
    await ctx.send(pyjokes.get_joke())

@client.command(name='hello', help='This command returns a random welcome message')
async def hello(ctx):
    responses = ['**Hey Bro**', '***Hello Hello Hello***', '**Wasssuup!**', '**Noiccee**']
    await ctx.send(choice(responses))

@client.command(name='die', help='This command returns a random last words')
async def die(ctx):
    responses = ['why have you brought my short life to an end', 'i could have done so much more', 'i have a family, kill them instead']
    await ctx.send(choice(responses))

@client.command(name='credits', help='This command returns the credits')
async def credits(ctx):
    await ctx.send('Made by `Attu_patil`')

@client.command(name='create-channel')
@commands.has_role('Admin')
async def create_channel(ctx, channel_name='home'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'The New Channel is created under name:- {channel_name}')
        await guild.create_text_channel(channel_name)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Sorry mate you dont have permission.')

@client.command(name='play', help='This command plays music')
async def play(ctx, url):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel Please Connect to voice")
        return
    
    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

    server = ctx.message.guild
    voice_channel = server.voice_client
    
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=client.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('**Now playing:** {}'.format(player.title))

@client.command(name='stop', help='This command stops the music and makes the bot leave the voice channel')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

@client.command(name='xkcd', help='Gets a random XKCD comic')
async def xkcd(ctx, arg):
    if arg == 'random':
        random = requests.get('https://c.xkcd.com/random/comic')
        comic = requests.get(random.url + 'info.0.json')
        await ctx.send(comic.json().get('img', 'No image available'))

    elif arg.isnumeric():
        comic = requests.get(f'https://xkcd.com/{arg}/info.0.json')
        if not str(comic.status_code).startswith('2'):
            await ctx.send(f'XKCD comic "{arg}" does not exist')

        else:
            await ctx.send(comic.json().get('img', 'No image available'))

    else:
        await ctx.send('Invalid argument: ' + str(arg))
# to get corona data use corona "NAME OF COUNTRY"
@client.command(name='corona', help='Gets you Corona Virus data')       
async def Data(ctx,coun):
    embed=discord.Embed(
        title = 'Covid Data about '+ coun,
        description='',
        color= discord.Color.dark_gold()
    )
    data=cov.get_status_by_country_name(coun)
    def Val(k):
        for key, value in data.items():
            if k == key:
                return value
    embed.set_footer(text=cov.source)
    embed.set_thumbnail(url='https://ahmednafies.github.io/covid/img/corona.jpeg')
    embed.set_image(url='https://ahmednafies.github.io/covid/img/corona.jpeg')
    embed.set_author(name='Covid Data',
                    icon_url='https://upload.wikimedia.org/wikipedia/commons/9/97/The_Earth_seen_from_Apollo_17.jpg')
    embed.add_field(name='Total Confirmed Cases', value=Val('confirmed'), inline=False)
    embed.add_field(name='Active Cases',value=Val('active'),inline=False)
    embed.add_field(name='No.of Deaths', value=Val('deaths'), inline=False)
    embed.add_field(name='Recovered', value=Val('recovered'), inline=False)
    await ctx.send(embed=embed)
        
@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))

client.run('')
