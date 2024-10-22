import discord
from discord.ext import commands
import random

bot = commands.Bot(command_prefix = "j!", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("bot ready")

@bot.command()
async def hello(ctx):
    await ctx.send(f"hello baka {ctx.author.mention}!")

@bot.command()
async def myhelp(ctx):
    await ctx.send(f"so you need some help working this bot ehh {ctx.author.mention}!")
    await ctx.send(f"Type `j!` as prefixed")
    await ctx.send(f"`myhelp`, `drop`, `inventory`, `cooldowns`, `rarity`")

#Function to determine card droprate !!
def droprate():
    random_number = random.randint(1, 10000)
    rarity = ""

    if random_number > 9899:  # 0.1% for LR
        rarity = "LR"
    elif random_number > 9798:  # 1.01% for UR
        rarity = "UR"
    elif random_number > 8998:  # 8% for SSR
        rarity = "SSR"
    elif random_number > 7998:  # 10% for SR
        rarity = "SR"
    elif random_number > 4998:  # 30% for R
        rarity = "R"
    else:  # 50% for N
        rarity = "N"
    
    return rarity

# Cards in each rarity
card_pool = {
    'N': ['SideCharacter (N)', 'SideCharacter2 (N)'],
    'R': ['PyroStark (R)', 'Rukironii (R)', 'Branakuya (R)'],
    'SR': ['Lensu (SR)', 'Munozaki (SR)'],
    'SSR': ['TomKuna (SSR)', 'Shinrago (SSR)', 'GrimDrago (SSR)'],
    'UR': ['YachiTuan (UR)'],
    'LR': ['Diddy Force (LR)']
}


#drop command! hope this works
@bot.command()
async def drop(ctx):
    cardRarity = droprate()
    card = random.choice(card_pool[cardRarity])

    await ctx.send(f"You've dropped **{card}**! Yippee!")


# load token from file and start botn ***KEEP AT BOTTOM***
with open("token.txt") as file:
    token = file.read()

bot.run(token)