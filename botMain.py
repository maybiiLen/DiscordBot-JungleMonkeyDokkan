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
card_poolMatsuri = {
    'N': [
        {'name': 'NPC (N)', 'image': 'theImage'},
        {'name': 'NPC2 (N)', 'image': 'theImage'}  
    ],
    'R': [
        {'name': 'PyroStark (R)', 'image': 'theImage'},
        {'name': 'Edku (R)', 'image': 'theImage'},
        {'name': 'Rukironii (R)', 'image': 'theImage'},
        {'name': 'Branakuya (R)', 'image': 'theImage'},
        {'name': 'Munozaki (SR)', 'image': 'theImage'},
        {'name': 'Tasugaya (SR)', 'image': 'theImage'}
    ],
    'SR': [
        {'name': 'IchiLen (SR)', 'image': 'theImage'},
        {'name': 'PyroStark (SR)', 'image': 'theImage'},
        {'name': 'Tosuke (SR)', 'image': 'theImage'},
        {'name': 'GrimDrago (SSR)', 'image': 'theImage'}
    ],
    'SSR': [
        {'name': 'Lentsu (SSR)', 'image': 'theImage'},
        {'name': 'Shinrago (SSR)', 'image': 'theImage'}
    ],
    'UR': [
        {'name': 'YachiTuan (UR)', 'image': 'theImage'},
        {'name': 'TomKuna (SSR)', 'image': 'theImage'}
    ],
    'LR': [
        {'name': 'Diddy Force (LR)', 'image': 'theImage'},
        {'name': 'FireDuo (LR)', 'image': 'theImage'}
    ]
}


#getting the rarity to choose which pool
def card_drop():
    cardRarity = droprate()
    card = random.choice(card_poolMatsuri[cardRarity])
    return cardRarity, card

#drop command! hope this works
@bot.command()
#@commands.cooldown(1, 1800, commands.BucketType.user)  # Cooldown set to 1800 seconds (30 minutes)
async def drop(ctx):
    cardRarity, card = card_drop()  # Get the card and its rarity

    # Send the message about the card
    await ctx.send(f'You got a {cardRarity} card: {card["name"]} {ctx.author.mention}!')

    # Check if the card has an image and display it as an embed(in frame)
    if card['image']:
        embed = discord.Embed()  
        embed.set_image(url=card['image'])  
        await ctx.send(embed=embed) 

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