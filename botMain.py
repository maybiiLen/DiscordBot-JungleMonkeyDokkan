import discord
from discord.ext import commands
import random
import asyncio

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
    await ctx.send(f"`myhelp`, `drop`, `inventory`, `cooldowns`, `rarity`,")

#Function to determine card droprate !!
def droprate():
    random_number = random.randint(1, 10000)

    if random_number > 9899:  # 0.1% for LR
        return "LR"
    elif random_number > 9798:  # 1.01% for UR
        return "UR"
    elif random_number > 8998:  # 8% for SSR
        return "SSR"
    elif random_number > 7998:  # 10% for SR
        return "SR"
    elif random_number > 4998:  # 30% for R
        return "R"
    else:  # 50% for N
        return "N"

# Cards in each rarity
card_pool = {
    'N': ['SideCharacter (N)', 'SideCharacter2 (N)'],
    'R': ['PyroStark (R)', 'Rukironii (R)', 'Branakuya (R)'],
    'SR': ['Lensu (SR)', 'Munozaki (SR)'],
    'SSR': ['TomKuna (SSR)', 'Shinrago (SSR)', 'GrimDrago (SSR)'],
    'UR': ['YachiTuan (UR)'],
    'LR': ['Diddy Force (LR)']
}


#getting the rarity to choose which pool
def card_drop():
    cardRarity = droprate()
    card = random.choice(card_pool[cardRarity])
    return cardRarity, card

#drop command! hope this works
@bot.command()
@commands.cooldown(1, 1800, commands.BucketType.user)  # Cooldown set to 1800 seconds (30 minutes)
async def drop(ctx):
    cardRarity, card = card_drop()  # Get the card and its rarity
    await ctx.send(f'You got a {cardRarity} card: {card} {ctx.author.mention}!')

#wait! you just drop
@drop.error
async def drop_error(ctx, error):
    if isinstance(error,commands.CommandOnCooldown):
        await ctx.send(f'chill out bro, im on cooldown. gimme {round(error.retry_after / 60)} minutes.')

#Checking cooldown of bot
@bot.command()
async def cooldown(ctx):
    if drop.is_on_cooldown(ctx):
        await ctx.send(f'Cooldown: {round(drop.get_cooldown_retry_after(ctx) / 60)} minutes.')
    else:
        await ctx.send(f'start dropping buddy.')


# load token from file and start botn ***KEEP AT BOTTOM***
with open("token.txt") as file:
    token = file.read()

bot.run(token)