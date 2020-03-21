import os
import discord
import json

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
CONFIG_JSON = os.environ.get('CONFIG_JSON')


def log_message(guild, message):
    datetime_now = datetime.now()
    print(str(datetime_now) + " - " + f'{guild.name}#{guild.id}: {message}')


def get_config():
    config = None
    with open(CONFIG_JSON) as config_json:
        config = json.load(config_json)

    return config


# setup command prefix
command_prefix = get_config()['command_prefix']
lfg_bot = commands.Bot(command_prefix='!')

lfg_command = get_config()['lfg_command']


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


@lfg_bot.command(name=lfg_command)
async def add_id(ctx):
    guild = ctx.guild
    channel = ctx.channel
    author = ctx.author
    command = ctx.message.content

    log_message(guild, f'"{command_prefix}{lfg_command}" executed by "{author}" in "{channel}#{channel.id}"')

        # delete message containing the command
    #await ctx.message.delete()



lfg_bot.run(DISCORD_TOKEN)
