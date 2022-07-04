import configparser
import datetime
import logging
import os.path
import platform
import sys
import time

import discord
from discord.ext import commands

#logging config
logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)

#try to find ini file, create if it does not exist
config = configparser.ConfigParser()
if not os.path.isfile('config.ini'):
    print("The file 'config.ini' does not exist! Creating one with default values")
    config['BOT CONFIG'] = {'prefix': '!', 'owner': '', 'token': ''}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    sys.exit("Please edit the file 'config.ini' and add your bot's token and owner's ID")

#read config file, store data into variables
config.read('config.ini')
bot_config = config['BOT CONFIG']
prefix = bot_config['prefix']
owner_id = bot_config['owner']
token = bot_config['token']
#make sure token, owner id are not empty
if token == '' or owner_id == '':
    sys.exit("Please edit the file 'config.ini' and add your bot's token and owner's ID")

#intents, initialize bot
intents = discord.Intents.default()
intents.messages = True
intents.members = True
bot = commands.Bot(command_prefix=prefix, intents=intents)

#load cogs
extensions = [
    'cogs.config',
]
logging.info("Loading cogs...")
for extension in extensions:
    try:
        bot.load_extension(extension)
        logging.info(f"Loaded cog {extension}")
    except commands.ExtensionNotFound:
        logging.info(f"Cog {extension} not found")
logging.info("Cogs loaded!")

#on_ready event
@bot.event
async def on_ready():
    bot.startTime = time.time()
    bot.owner = bot.get_user(int(owner_id))
    bot.restart = False #do not restart by default
    logging.info(f"Bot started! Hello {str(bot.owner)}!")

#about command
@bot.command()
async def about(ctx):
    uptime = int(round(time.time() - bot.startTime))
    uptime = datetime.timedelta(seconds=uptime)
    embed = discord.Embed(title="Heathcliff Bot", description="A discord bot for the People's Republic of Garfield", color=0x00ff00)
    embed.add_field(name=":crown: Owner", value=str(bot.owner), inline=False)
    embed.add_field(name=":clock: Uptime", value=str(uptime), inline=False)
    embed.add_field(name=":computer: Platform", value=str(platform.platform()), inline=False)
    embed.add_field(name=":snake: Python Version", value=str(platform.python_version()), inline=False)
    await ctx.send(embed=embed)

#reload cogs
@bot.command(aliases=['rl', 'reload'])
async def reload_cog(ctx, cog: str):
    """Reloads a cog"""
    try:
        bot.unload_extension(f'cogs.{cog}')
        bot.load_extension(f'cogs.{cog}')
        await ctx.send(f"Reloaded cog \"{cog}\"!")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

bot.run(token)

if bot.restart == False:
    sys.exit(0)
else:
    sys.exit(1)
