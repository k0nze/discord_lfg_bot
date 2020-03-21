import os
import discord

from datetime import datetime
from discord.utils import get
from discord.ext import commands
from os.path import join, dirname
from dotenv import load_dotenv

# load .env file
dir_path = os.path.dirname(os.path.realpath(__file__))

dotenv_path = join(dir_path, '.env')
load_dotenv(dotenv_path)

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')


lfg_bot = commands.Bot(command_prefix='!lfg')


def log_message(guild, message):
    datetime_now = datetime.now()
    print(str(datetime_now) + " - " + f'{guild.name}#{guild.id}: {message}')
 

@lfg_bot.event
async def on_ready():

    print(str(datetime.now()) + " - " + f'{lfg_bot.user.name} has connected to Discord')

    # check if bot has connected to guilds
    if len(lfg_bot.guilds) > 0:
        print('connected to the following guilds:')

        for guild in lfg_bot.guilds:
            print(f'* {guild.name}#{guild.id}')

    # set activitiy
    await lfg_bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="git.io/JvMhj"))


lfg_bot.run(DISCORD_TOKEN)
