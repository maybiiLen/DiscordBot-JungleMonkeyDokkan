import discord
from discord.ext import commands
import random
import asyncio
from collections import defaultdict
import json
import aiofiles
import signal 


bot = commands.Bot(command_prefix = ["j!", "j"], intents = discord.Intents.all())

userInventory = defaultdict(lambda: defaultdict(int))

userCooldowns = {}

# Global dictionary for colors based on full rarity names
rarity_colors = {
    'Legendary Rare': discord.Color.gold(),
    'Ultra Rare': discord.Color.red(),
    'Super Super Rare': discord.Color.purple(),
    'Super Rare': discord.Color.blue(),
    'Rare': discord.Color.pink(),
    'Normal': discord.Color.green()
}

@bot.event
async def on_ready():
    print("bot ready")
    try: 
        async with aiofiles.open('playerInventory.json', 'r') as file:
            data = await file.read()
            if data:
                loaded_inventory = json.loads(data)
                for user_id, cards in loaded_inventory.items():
                    for card_name, count in cards.items():
                        userInventory[int(user_id)][card_name] = count
                print("Inventory loaded successfully")
    except FileNotFoundError:
        print("oh so your new huh?, we're gonna be starting with a fresh inventory")

    bot.loop.create_task(save_inventory())
    bot.loop.create_task(cooldown_alert())


async def writeToFiles():
    try:
        normal_dict = {k: dict(v) for k, v in userInventory.items()}
        async with aiofiles.open('playerInventory.json', 'w') as file:
            await file.write(json.dumps(normal_dict, indent=4))  # Added indent for readability
        print("Inventory saved!!")
    except Exception as e:
        print(f"error saving inventory: {e}")


async def save_inventory():
    while True:
        await writeToFiles()
        await asyncio.sleep(3600)


#bot shutdown command 

def bot_shutdown_signal(signal_received, frame):
    bot.loop.create_task(writeToFiles())
    bot.loop.create_task(bot.close())

signal.signal(signal.SIGINT, bot_shutdown_signal)
signal.signal(signal.SIGTERM, bot_shutdown_signal)

#reset inventory command
@bot.command()
async def fullreset(ctx):
    if ctx.author.guild_permissions.administrator:
        userInventory.clear()
        await writeToFiles()
        await ctx.send(f"Inventory has been reset")
    else:
        await ctx.send(f"ayyy, u dont got perms lil bro")



@bot.command()
async def hello(ctx):
    await ctx.send(f"hello baka {ctx.author.mention}!")

@bot.command()
async def myhelp(ctx):
    await ctx.send(f"so you need some help working this bot ehh {ctx.author.mention}!")
    await ctx.send(f"Type `j!` as prefixed")
    await ctx.send(f"`myhelp`, `drop`, `inventory`, `cooldown`, `rarity`, `view`")

#Function to determine card droprate !!
def droprate():
    random_number = random.randint(1, 100000)  # Extend the range to 100,000
    
    if random_number == 1:  # 0.001% for secret rarity
        return "Secret"
    elif random_number <= 1001:  # 1% for LR (from 2 to 1001)
        return "Legendary Rare"
    elif random_number <= 4001:  # 3% for UR (from 1002 to 4001)
        return "Ultra Rare"
    elif random_number <= 10001:  # 6% for SSR (from 4002 to 10001)
        return "Super Super Rare"
    elif random_number <= 20001:  # 10% for SR (from 10002 to 20001)
        return "Super Rare"
    elif random_number <= 50001:  # 30% for R (from 20002 to 50001)
        return "Rare"
    else:  # 50% for N (from 50002 to 100000)
        return "Normal"



# Cards in each rarity
card_poolMatsuri = {
    'Normal': [
        {'name': 'NPC (N)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298473330592186418/NPC_N_1.png?ex=6719b106&is=67185f86&hm=582e828418f2c1f6d470fa235bdc35f6b65f931a8e2344242b8f5febc8830460&=&format=webp&quality=lossless'},
        {'name': 'NPC2 (N)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298475633331933257/NPC2N.png?ex=6719b32b&is=671861ab&hm=f72ebc3d4b911b60f483548b6789fc9d1e8953d7f5eb9231629c95ad79a72650&=&format=webp&quality=lossless'}  
    ],
    'Rare': [
        {'name': 'Edku (R)', 'image': 'https://media.discordapp.net/attachments/1276598824579629089/1300641039308034138/edku_2024_ed_1.png?ex=672193dc&is=6720425c&hm=e2dce11f68f305c4ef564093fb1bb4adfcc82fd06cab4bcba24068bb48467d39&=&format=webp&quality=lossless'},
        {'name': 'Rukironii (R)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298479345823912057/RukironiiR.png?ex=6719b6a0&is=67186520&hm=d8db71182428ac2b54bed7c34f6dd8caa115d8c7fd7ef80af5d37c36c36a6546&=&format=webp&quality=lossless'},
        {'name': 'Branakuya (R)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298481165979619348/BranakuyaR.png?ex=6719b852&is=671866d2&hm=333d917bf25a2ca1dfa542c1f6a12b7806d3236394edcb8759d47bdeec6157b4&=&format=webp&quality=lossless'},
        {'name': 'Munozaki (R)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298481885164470303/MunozakiR.png?ex=6719b8fe&is=6718677e&hm=27bbb7cd857de83772ca96cf52f1564972c3a291f18c58ace649a0349b504105&=&format=webp&quality=lossless'},
        {'name': 'Tasugaya (R)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298482840945823844/TasugayaR.png?ex=6719b9e1&is=67186861&hm=77a2a35441e0cd5d36312b55371e8b3de5556e120c791c88a43e2ea18eed3b8e&=&format=webp&quality=lossless'}
    ],
    'Super Rare': [
        {'name': 'IchiLen (SR)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298484787081646091/IchilenSR.png?ex=6719bbb1&is=67186a31&hm=865d66c3f367d91062326dd135218dfd255ca4943dbaf80206074cd30829a1ee&=&format=webp&quality=lossless'},
        {'name': 'PyroStark (SR)', 'image': 'https://media.discordapp.net/attachments/1276598824579629089/1299893392393633802/PyroStarrk_2023_ed_1.png?ex=6720d5cf&is=671f844f&hm=f08c6e651e4fbbc0d5d7224cf9094f7b2b5125bf3cc8b848030a08303d1ff14d&=&format=webp&quality=lossless'},
        {'name': 'Tomsuke (SR)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298487049162330163/TomsukeSR.png?ex=6719bdcd&is=67186c4d&hm=8844e2d667d26121c302ba7660cbac9fccd439ad18c94aef7f6d1460cd0a05d6&=&format=webp&quality=lossless'},
        {'name': 'GrimDrago (SR)', 'image': 'https://media.discordapp.net/attachments/1276598824579629089/1299890763253022732/Dokkan_Template_PSD-SS.png?ex=671f81dc&is=671e305c&hm=38fb3e586405e56d8d499d8038aff6ef5e45c50543b30003d784a2cc49d7b843&=&format=webp&quality=lossless'}
    ],
    'Super Super Rare': [
        {'name': 'Lentsu (SSR)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298491074179764234/LentsuSSR.png?ex=6719c18c&is=6718700c&hm=2a57dfdf38eb57df6caf35fd499bee6650f3e2366d48cfe4e30a269dfe72716d&=&format=webp&quality=lossless'},
        {'name': 'Shinrago (SSR)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298493745137975336/ShinragowSSR.png?ex=6719c409&is=67187289&hm=8b6cfe16a4dd86fa83be595273c771e1d5fcbe6361e94d3a7c47995496455008&=&format=webp&quality=lossless'}
    ],
    'Ultra Rare': [
        {'name': 'YachiTuan (UR)', 'image': 'https://media.discordapp.net/attachments/1276598824579629089/1299999236347269161/tuanchiru_2023_ed_1.png?ex=671fe6e2&is=671e9562&hm=32c079102aaf5979d2fb455186bf6f8e291eca711cc96f30f913dac6456a9d27&=&format=webp&quality=lossless'},
        {'name': 'TomKuna (UR)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1298499485864824882/TomkunaUR.png?ex=6719c962&is=671877e2&hm=3ecfc0c9949027f2ad99d8d6360a86966cbf68046cb359326ef32c671eb291ff&=&format=webp&quality=lossless'}
    ],
    'Legendary Rare': [
        {'name': 'Diddy Force (LR)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1299265626744950804/DiddyForceLR_2.png?ex=671c92e8&is=671b4168&hm=254223a79a0deabc518fde99f8c7314c098ac627f3c4bfcaf45ecdc3bd0e7bb7&=&format=webp&quality=lossless'},
        {'name': 'FireDuo (LR)', 'image': 'https://media.discordapp.net/attachments/1298473140774637640/1299253759402311701/FireDuoLR.png?ex=671c87db&is=671b365b&hm=acef3ffa6cda2ebf8e4c8224f07c34e89ba13a05ab9bcc62863f82e4ffa8e4b9&=&format=webp&quality=lossless'}
    ]
}


#getting the rarity to choose which pool
def card_drop():
    cardRarity = droprate()
    card = random.choice(card_poolMatsuri[cardRarity])
    return cardRarity, card

#drop command! hope this works
@bot.command(aliases=["d"])
@commands.cooldown(1, 1800, commands.BucketType.user)  # Cooldown set to 1800 seconds (30 minutes)
async def drop(ctx):
    cardRarity, card = card_drop()  # Get the card and its rarity

    userInventory[ctx.author.id][card['name']] += 1

    cooldown_end = asyncio.get_event_loop().time() + 1800 
    userCooldowns[ctx.author.id] = (cooldown_end, ctx.channel)

    # Send the message about the card
    await ctx.send(f'You just drop a {cardRarity} Card: {card["name"]} {ctx.author.mention}!')

    color = rarity_colors.get(cardRarity, discord.Color.default())

    # Check if the card has an image and display it as an embed(in frame)
    if card['image']:
        embed = discord.Embed(color=color)  
        embed.set_image(url=card['image'])  
        await ctx.send(embed=embed) 

#cheecking for cooldown alert
async def cooldown_alert():
    await bot.wait_until_ready()
    while not bot.is_closed():
        current_time = asyncio.get_event_loop().time()

        for user_id, (cooldown_end, channel) in list(userCooldowns.items()):
            if current_time >= cooldown_end:
                user = await bot.fetch_user(user_id)
                await channel.send(f"{user.mention}, ayyy start dropping lil bro")

                del userCooldowns[user_id]

        await asyncio.sleep(60)
        
#wait! you just drop
@drop.error
async def drop_error(ctx, error):
    if isinstance(error,commands.CommandOnCooldown):
        print("cooldown is active")
        await ctx.send(f'chill out bro, im on cooldown. gimme {round(error.retry_after / 60)} minutes.')

#Checking cooldown of bot
@bot.command(aliases=["cd"])
async def cooldown(ctx):
    if drop.is_on_cooldown(ctx):
        await ctx.send(f'just busted a load, {round(drop.get_cooldown_retry_after(ctx) / 60)} minutes.')
    else:
        await ctx.send(f'start dropping buddy.')

#Inventory tracking
@bot.command(aliases=["i"])
async def inventory(ctx):
    user_inventory = userInventory[ctx.author.id]

    if not user_inventory:
        await ctx.send(f'damn {ctx.author.mention}, you aint got nun in here')
        return 
    else:
        embed = discord.Embed(title="Player's Inventory:\n",color = discord.Color.dark_purple())

        #showwing rank of rarity
        rarity_rank = {
            'LR': 1, 'UR': 2, 'SSR': 3, 'SR': 4, 'R': 5, 'N': 6
        }

        sort_inventory = sorted(user_inventory.items(), key=lambda item: (rarity_rank.get(item[0].split()[-1].strip("()"), 7), item[0]))

        displayInventory = ""
        for card_name, count in sort_inventory:
            displayInventory += f"{card_name} - {count}x\n"

        embed.add_field(name="Cards", value = displayInventory, inline = False)

    await ctx.send(embed=embed)

#viewing card image
@bot.command(aliases=["v"])
async def view(ctx, * , card_name: str):
    user_inventory = userInventory[ctx.author.id]
    card_found = False

    for name, count in user_inventory.items():
        if name.split(" ")[0].lower() == card_name.lower():
            for rarity, card_list in card_poolMatsuri.items():
                for card in card_list:
                    if card["name"] == name:
                        cardColor = rarity_colors.get(rarity, discord.Color.default())
                        embed = discord.Embed(title=f"{card['name']}", color=cardColor)
                        embed.set_image(url=card["image"])
                        await ctx.send(embed=embed)
                        card_found = True
                        break
                if card_found:
                    break
            break
    if not card_found:
        await ctx.send(f"ayyo lil bro, you aint got '{card_name}' in your inventory xD")


#showing rarity of card
@bot.command(aliases=["rar"])
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
    embed.add_field(name="SSR (Super Super Rare)", value="6% droprate", inline=False)
    embed.add_field(name="UR (Ultra Rare)", value="3% droprate", inline=False)
    embed.add_field(name="LR (Legendary Rare)", value="1% droprate", inline=False)


    await ctx.send(embed=embed)


# load token from file and start botn ***KEEP AT BOTTOM***
with open("token.txt") as file:
    token = file.read()

bot.run(token)