import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = "gatcha", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("bot ready")

with open("token.txt") as file:
    token = file.read()

bot.run(token)