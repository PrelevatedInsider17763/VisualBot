import os
import discord
from discord.ext import commands

# Check if the bot token is available as an environment variable
bot_token = os.environ.get("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

if not bot_token:
    print("Bot token not found. Please set the BOT_TOKEN environment variable.")
    exit(1)

@bot.command(name="crash")
async def crash(ctx):
    """Shut down the bot."""
    await bot.close()

@bot.command(name="ping")
async def ping(ctx):
    """Check if the bot is responsive."""
    await ctx.send('pong')

@bot.command(name="echo")
async def echo(ctx, *, string):
    """Repeat a message."""
    await ctx.send(string)

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """Kick a member from the server."""
    await member.kick(reason=reason)
    await ctx.send(f"{member} kicked from this server because **{reason}**.")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User, *, reason=None):
    """Ban a member from the server."""
    await ctx.guild.ban(member, reason=reason)
    await ctx.send(f"{member} banned from this server because **{reason}**.")

@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, member: discord.User, *, reason=None):
    """Unban a member from the server."""
    await ctx.guild.unban(member, reason=reason)
    await ctx.send(f"{member} unbanned because **{reason}**.")

@bot.event
async def on_message(message):
    """Automod function to filter messages."""
    if message.author == bot.user or message.author.guild_permissions.administrator:
        return  # Ignore messages from the bot itself or administrators

    server = message.guild
    data = read_json("automod.json")
    automod = data["automodservers"]

    if server.id in automod:
        raid_words = ['raid', 'raiding', 'spam', 'mass mention', 'invite', 'join']
        
        if any(word in message.content.lower() for word in raid_words):
            await message.delete()
            embed = discord.Embed(
                title=f"{message.author}, Your message contains content that is not allowed here!",
                description="Please refrain from using raid-related words.",
                color=discord.Color.red()
            )
            embed.set_footer(
                text="Automod made by: NotAlexy_Kyu#4003, and modified by: PrelevatedInsider17763#5707"
            )
            embed.set_image(url="https://www.kindpng.com/picc/m/65-650060_no-entry-png-transparent-png.png")
            await message.channel.send(embed=embed)

@bot.command()
async def hello(ctx, member: discord.Member):
    """Say hello to a specific member."""
    await ctx.send(f'Hello, {member.mention}!')

def read_json(filename):
    """Read JSON data from a file."""
    with open(filename, "r") as f:
        data = json.load(f)
    return data

def write_json(data, filename):
    """Write JSON data to a file."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

bot.run(bot_token)
