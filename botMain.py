import discord
from discord.ext import commands
import random
import asyncio
from collections import defaultdict
import json
import os 

bot = commands.Bot(command_prefix = "j!", intents = discord.Intents.all())

#delcare inventory
inventory_file = 'savedInventory.json'

userInventory = defaultdict(lambda: defaultdict(int))

#loading and saving inventory into json file
def load_inventory():
    global userInventory
    if os.path.exists(inventory_file):
        if os.path.getsize(inventory_file) > 0:  # Check if the file is not empty
            with open(inventory_file, 'r') as file:
                try:
                    data = json.load(file)
                    # Convert the loaded data back into a defaultdict
                    userInventory = defaultdict(lambda: defaultdict(int), {k: defaultdict(int, v) for k, v in data.items()})
                    print("Inventory loaded successfully.")
                except json.JSONDecodeError:
                    print("Error loading JSON data.")
        else:
            print("Inventory file is empty. Starting with an empty inventory.")
    else:
        print("No inventory file found. Starting with an empty inventory.")


def save_inventory():
    with open(inventory_file, 'w') as file:
        json.dump({k: dict(v) for v in userInventory.items()}, file, indent=4)

#starting the bot
@bot.event
async def on_ready():
    print("bot ready")
    load_inventory()

#saving file on disconnect
@bot.event
async def on_disconnect():
    save_inventory()

@bot.command()
async def hello(ctx):
    await ctx.send(f"hello baka {ctx.author.mention}!")

@bot.command()
async def myhelp(ctx):
    await ctx.send(f"so you need some help working this bot ehh {ctx.author.mention}!")
    await ctx.send(f"Type `j!` as prefixed")
    await ctx.send(f"`myhelp`, `drop`, `inventory`, `cooldown`, `rarity`, `view`")

#Function to determine card droprate !!
import random
def droprate():
    random_number = random.randint(1, 100000)  # Extend the range to 100,000
    
    if random_number == 1:  # 0.001% for secret rarity
        return "Secret"
    elif random_number <= 1001:  # 1% for LR (from 2 to 1001)
        return "Legendary Rare"
    elif random_number <= 4001:  # 3% for UR (from 1002 to 4001)
        return "Ultra Rare" 
    elif random_number <= 12001:  # 8% for SSR (from 4002 to 12001)
        return "Super Super Rare"
    elif random_number <= 22001:  # 10% for SR (from 12002 to 22001)
        return "Super Rare"
    elif random_number <= 52001:  # 30% for R (from 22002 to 52001)
        return "Rare"
    else:  # 50% for N (from 52002 to 100000)
        return "Normal"

# Cards in each rarity
card_poolMatsuri = {
    'Normal': [
        {'name': 'NPC (N)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298473330592186418/NPC_N_1.png?ex=671a59c6&is=67190846&hm=662153b1a255eb94e67859a7e9c6f27b4d7efb05dbce6104b801db617c613210&=&format=webp&quality=lossless'},
        {'name': 'NPC2 (N)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298475633331933257/NPC2N.png?ex=6719b32b&is=671861ab&hm=f72ebc3d4b911b60f483548b6789fc9d1e8953d7f5eb9231629c95ad79a72650&=&format=webp&quality=lossless'}  
    ],
    'Rare': [
        {'name': 'Edku (R)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298478583123021834/EdkuR.png?ex=6719b5ea&is=6718646a&hm=db00227e28e8b1c813dd365fbd92c4f52a87837717e7af7baddc9c228b29f84f&=&format=webp&quality=lossless'},
        {'name': 'Rukironii (R)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298479345823912057/RukironiiR.png?ex=6719b6a0&is=67186520&hm=d8db71182428ac2b54bed7c34f6dd8caa115d8c7fd7ef80af5d37c36c36a6546&=&format=webp&quality=lossless'},
        {'name': 'Branakuya (R)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298481165979619348/BranakuyaR.png?ex=6719b852&is=671866d2&hm=333d917bf25a2ca1dfa542c1f6a12b7806d3236394edcb8759d47bdeec6157b4&=&format=webp&quality=lossless'},
        {'name': 'Munozaki (SR)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298481885164470303/MunozakiR.png?ex=6719b8fe&is=6718677e&hm=27bbb7cd857de83772ca96cf52f1564972c3a291f18c58ace649a0349b504105&=&format=webp&quality=lossless'},
        {'name': 'Tasugaya (SR)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298482840945823844/TasugayaR.png?ex=6719b9e1&is=67186861&hm=77a2a35441e0cd5d36312b55371e8b3de5556e120c791c88a43e2ea18eed3b8e&=&format=webp&quality=lossless'}
    ],
    'Super Rare': [
        {'name': 'IchiLen (SR)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298484787081646091/IchilenSR.png?ex=6719bbb1&is=67186a31&hm=865d66c3f367d91062326dd135218dfd255ca4943dbaf80206074cd30829a1ee&=&format=webp&quality=lossless'},
        {'name': 'PyroStark (SR)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298486247190302784/PyrostarkSR.png?ex=6719bd0e&is=67186b8e&hm=037986c3ad28284b2c46ae1f07422d13f58ebce9a50c3e3a361eee8d810dafa9&=&format=webp&quality=lossless'},
        {'name': 'Tomsuke (SR)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298487049162330163/TomsukeSR.png?ex=6719bdcd&is=67186c4d&hm=8844e2d667d26121c302ba7660cbac9fccd439ad18c94aef7f6d1460cd0a05d6&=&format=webp&quality=lossless'},
        {'name': 'GrimDrago (SSR)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298487983942533150/GrimdragoSR.png?ex=6719beac&is=67186d2c&hm=8c5b127904d6ac94c9082f048c1b7a957bbab9332d68faf268811c02523a45b2&=&format=webp&quality=lossless'}
    ],
    'Super Super Rare': [
        {'name': 'Lentsu (SSR)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298491074179764234/LentsuSSR.png?ex=6719c18c&is=6718700c&hm=2a57dfdf38eb57df6caf35fd499bee6650f3e2366d48cfe4e30a269dfe72716d&=&format=webp&quality=lossless'},
        {'name': 'Shinrago (SSR)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298493745137975336/ShinragowSSR.png?ex=6719c409&is=67187289&hm=8b6cfe16a4dd86fa83be595273c771e1d5fcbe6361e94d3a7c47995496455008&=&format=webp&quality=lossless'}
    ],
    'Ultra Rare': [
        {'name': 'YachiTuan (UR)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298496837690331147/YachituanUR.png?ex=6719c6eb&is=6718756b&hm=61a2c727deb998401d865b7b7c334d5971d987ce1ca957b2d2b47ff009d25eb8&=&format=webp&quality=lossless'},
        {'name': 'TomKuna (SSR)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298499485864824882/TomkunaUR.png?ex=6719c962&is=671877e2&hm=3ecfc0c9949027f2ad99d8d6360a86966cbf68046cb359326ef32c671eb291ff&=&format=webp&quality=lossless'}
    ],
    'Legendary Rare': [
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
@commands.cooldown(1, 1800, commands.BucketType.user)  # Cooldown set to 1800 seconds (30 minutes)
async def drop(ctx):
    cardRarity, card = card_drop()  # Get the card and its rarity

    userInventory[ctx.author.id][card['name']] += 1

    save_inventory()

    # Send the message about the card
    await ctx.send(f'You just drop a {cardRarity} Card: {card["name"]} {ctx.author.mention}!')

    if cardRarity == 'Legendary Rare':
        color=discord.Color.gold()
    elif cardRarity == 'Ultra Rare':
        color=discord.Color.red()
    elif cardRarity == 'Super Super Rare':
        color=discord.Color.pink()
    elif cardRarity == 'Super Rare':
        color=discord.Color.blue()
    elif cardRarity == 'Rare':
        color=discord.Color.purple()
    elif cardRarity == 'Normal':
        color=discord.Color.green()

    # Check if the card has an image and display it as an embed(in frame)
    if card['image']:
        embed = discord.Embed(color=color)  
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
        await ctx.send(f'just busted a load, {round(drop.get_cooldown_retry_after(ctx) / 60)} minutes.')
    else:
        await ctx.send(f'start dropping buddy.')

#Inventory tracking
@bot.command()
async def inventory(ctx):
    user_inventory = userInventory[ctx.author.id]

    if not user_inventory:
        await ctx.send(f'damn {ctx.author.mention}, you aint got nun in here')
        return 
    else:
        embed = discord.Embed(color = discord.Color.dark_blue())


        displayInventory = f"{ctx.author.mention}'s Inventory:\n"
        for card_name, count in user_inventory.items():
            embed.add_field(name = card_name, value = f"{count}x",inline=False)

    await ctx.send(displayInventory)
    await ctx.send(embed=embed)

#showing rarity of card
@bot.command()
async def rarity(ctx):
    # Create an embed object
    embed = discord.Embed(
        title="Card Rarity",
        description="**someone here didn't play Dokkan, don't worry, I've got you covered!**",
        color=discord.Color.blue()  # You can choose any color here
    )

    # Add fields for each rarity
    embed.add_field(name="N (Normal)", value="50% droprate", inline=False)
    embed.add_field(name="R (Rare)", value="30% droprate", inline=False)
    embed.add_field(name="SR (Super Rare)", value="10% droprate", inline=False)
    embed.add_field(name="SSR (Super Super Rare)", value="8% droprate", inline=False)
    embed.add_field(name="UR (Ultra Rare)", value="3% droprate", inline=False)
    embed.add_field(name="LR (Legendary Rare)", value="1% droprate", inline=False)


    await ctx.send(embed=embed)


# load token from file and start botn ***KEEP AT BOTTOM***
with open("token.txt") as file:
    token = file.read()

bot.run(token)