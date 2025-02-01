import discord
from discord.ext import commands, tasks
from discord import Embed
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Set up a simple welcome message
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='general')
    if channel:
        await channel.send(f"Welcome {member.mention}! We're happy to have you!")

# Define command for sticky messages
@bot.command()
async def sticky(ctx, *, message):
    await ctx.send(message)
    await asyncio.sleep(60)  # You can adjust the time interval
    await ctx.send(message)  # The message will repeat every 60 seconds

# Define command to send customizable embeds
@bot.command()
async def embed(ctx, title, description):
    embed = Embed(title=title, description=description, color=discord.Color.blue())
    await ctx.send(embed=embed)

# Auto-moderation: Basic profanity filter
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    profanities = ["badword1", "badword2", "badword3"]  # Replace these with actual words
    if any(word in message.content.lower() for word in profanities):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, please refrain from using inappropriate language.")
        return

    await bot.process_commands(message)

# Reaction Roles (assign roles based on reactions)
@bot.command()
async def reactionrole(ctx):
    message = await ctx.send("React to this message to get a role!")
    await message.add_reaction("👍")  # This emoji will trigger the role

    def check(reaction, user):
        return user != bot.user and str(reaction.emoji) == "👍"

    reaction, user = await bot.wait_for("reaction_add", check=check)
    role = discord.utils.get(ctx.guild.roles, name="Reacted")
    if role:
        await user.add_roles(role)
        await ctx.send(f"Assigned {role.name} to {user.mention}.")

# Reminders
@bot.command()
async def remind(ctx, time: int, *, reminder):
    await ctx.send(f"Reminder set for {time} minutes from now.")
    await asyncio.sleep(time * 60)
    await ctx.send(f"{ctx.author.mention}, here's your reminder: {reminder}")

# List all commands with a custom 'cmd' command
@bot.command()
async def cmd(ctx):
    help_message = """
    **List of Commands:**
    !sticky <message> - Sends a sticky message that repeats every 60 seconds.
    !embed <title> <description> - Sends a custom embed.
    !reactionrole - Sets up a reaction role.
    !remind <time in minutes> <reminder> - Sets a reminder.
    """
    await ctx.send(help_message)

# Start the bot
bot.run('YOUR_BOT_TOKEN')
