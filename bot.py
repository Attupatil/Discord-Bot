import discord
from discord.ext.commands import Bot
from discord.ext import commands

client = commands.Bot(command_prefix='>')

@client.command()
async def ping(ctx):
    await ctx.send(f'gap na bhava kiti trass detos!!__Bhau ahes mhnun boltoe nahitr nasto bolo.. {round(client.latency * 1000)}ms cha ping ahey tujha')

@client.command()
async def version(ctx):
    """Check the current bot version"""
    await ctx.send("You are running KDbot 1.0")

@client.command()
async def shoot(user_name : discord.User):
    """Shoot another player"""
    await client.say(f"*Shoots {user_name.mention} <a:pepeshoot:415631916361056256>")
    

@client.command()
async def on_member_join(member):
    print(f'{member}ha ek aala aata unadkyaa karaila')

@client.command()
async def on_member_move(member):
    print(f'{member}Acha hua chala gaya')
client.run('NzU0MjQ1ODMwMzc4MjU4NDMz.X1x8Kw.-3dpQ19jF7oHt7vnuTUTzeSG68A')
