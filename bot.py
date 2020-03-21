import os
import discord
import json
import re

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


async def send_command_error_message(member, additional_content):
    command_synopsis = get_config()['command_synopsis']
    command_synopsis = command_synopsis.replace('{command_prefix}', command_prefix)
    command_synopsis = command_synopsis.replace('{lfg_command}', lfg_command)

    dm_command_hint = get_config()['dm_command_hint']

    message_text = additional_content + "\n" + dm_command_hint + "\n" + command_synopsis

    channel = await member.create_dm()
    await channel.send(message_text)


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
    message = ctx.message
    command = ctx.message.content

    log_message(guild, f'"{command_prefix}{lfg_command}" executed by "{author}" in "{channel}#{channel.id}"')

    # check if command was issued in the correct channel
    lfg_channel_id = get_config()['lfg_channel_id']

    if channel.id != lfg_channel_id:
        log_message(guild, f'* command was ignored since it was not issued in the correct channel')
        return

    # check if command contains a role mention
    if len(message.role_mentions) < 1:
        dm_no_role_mentioned = get_config()['dm_no_role_mentioned'] 
        await send_command_error_message(author, dm_no_role_mentioned)
        await message.delete()
        log_message(guild, f'* command message was deleted since no role was mentioned in it')
        return
       
    # check if command contains a message
    lfg_message = command.replace(command_prefix, "")
    lfg_message = lfg_message.replace(lfg_command, "")
    lfg_message = re.sub('<@&[0-9]+>', '', lfg_message)
    lfg_message = lfg_message.lstrip()

    if len(lfg_message) == 0:
        dm_no_lfg_message = get_config()['dm_no_lfg_message'] 
        await send_command_error_message(author, dm_no_lfg_message)
        await message.delete()
        log_message(guild, f'* command message was deleted since no message was in it')
        return

    # check if command issuer is in a voice channel
    author_voice_channel = None

    for voice_channel in guild.voice_channels:
        if author_voice_channel is None: 
            for member in voice_channel.members:
                if member.id == author.id:
                    author_voice_channel = voice_channel
                    break;
           
    if author_voice_channel is None:
        dm_not_in_voice_channel = get_config()['dm_not_in_voice_channel'] 
        await send_command_error_message(author, dm_not_in_voice_channel)
        await message.delete()
        log_message(guild, f'* command message was deleted since author is not in a voice channel')
        return

    voice_channel_invite = await author_voice_channel.create_invite(max_age=int(get_config()['invite_max_age']))

    # generate invite message
    invite_message = ""

    # add mentioned roles to invite message
    for role_mention in message.role_mentions:
        invite_message = invite_message + f'<@&{role_mention.id}> '

    # add lfg message to invite message
    invite_message = invite_message + lfg_message + "\nfrom " 

    # add member which are in the voice channel to invite message
    for member in author_voice_channel.members:
        invite_message = invite_message + f'<@!{member.id}> '

    invite_message = invite_message 

    # send invite message
    await channel.send(invite_message)

    # send voice channel invite
    await channel.send(voice_channel_invite)  

    # delete message containting the command 
    await message.delete()

    log_message(guild, f'* invite has been created')


@lfg_bot.event
async def on_message(message):

    guild = message.guild
    author = message.author
    channel = message.channel

    # check if message is not a DM and not created by a bot
    if not isinstance(channel, discord.DMChannel) and not message.author.bot:

        lfg_channel_id = get_config()['lfg_channel_id']

        # check if message was send to the lfg channel and does not contain an lfg 
        if (channel.id == get_config()['lfg_channel_id']) and not (command_prefix + lfg_command in message.content):
            dm_no_lfg_command = get_config()['dm_no_lfg_command'] 
            await send_command_error_message(author, dm_no_lfg_command)
            await message.delete()
            log_message(guild, f'" message of "{author}" in "{channel}#{channel.id} was deleted since it did not contain a command"')
            return

        await lfg_bot.process_commands(message)


lfg_bot.run(DISCORD_TOKEN)
