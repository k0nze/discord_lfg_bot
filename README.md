# Discord Looking for Group Bot

This bot listens to the `!lfg` command in a specified channel and based on it creates an invite into a voice channel. The invite into a voice channel will be created if a role was mentioned and an invite message was added to the command. It also checks if the author of the invite is in a voice channel.

## Setup

Create a Discord application and bot in the Discord developer portal and make sure to set the following persmissions:

 * General Permissions
    * Manage Channels
    * Create Instant Invite
    * View Channels

 * Text Permissions
    * Send Messages
    * Manage Messages
    * Embed Links
    * Mention Everyone
    * Use External Emoji
    * Add Reactions

Under OAuth check _bot_.

Install necessary packages:

```bash
python3 -m pip install -r requirements.txt
```

Copy the `.env.sample` and replace `{discord-token}` with your bot's Discord token in `.env`

```bash
cp .env.sample .env
```

Copy the `config.json.sample` to `config.json` and Replace the following placeholders

| Name                      | Description |
| ------------------------- | ------------- |
| `command_prefix`          | On which command prefix should the bot be triggered |
| `lfg_command`             | Command after `command_prefix` which will generate a voice channel invite |
| `lfg_channel_id`          | ID of the channel to which the bot should listen to the LFG command: `command_prefix``lfg_command` |
| `command_synopsis`        | Explains how an LFG command should be structured. This will be send as a DM to a member who used command wrong |
| `dm_command_hint`         | Text that will be send before the `command_synopsis` in a DM |
| `dm_no_role_mentioned`    | Text that will be send before `dm_command_hint` in a DM if no role was mentioned in the LFG command |
| `dm_no_lfg_message`       | Text that will be send before `dm_command_hint` in a DM if no message was added to the LFG command |
| `dm_not_in_voice_channel` | Text that will be send before `dm_command_hint` in a DM if author of LFG command is not in a voice channel  |
| `dm_no_lfg_command`       | Text that will be send before `dm_command_hint` in a DM if author did not issue the LFG command in the LFG channel |
| `invite_max_age`          | How long should an invite be valid in seconds |
| `purge_messages_after`    | After how many seconds should and invite in the LFG channel deleted |


## Run
```bash
python3 bot.py
```
