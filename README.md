# Discord LFG Bot
## Setup
Install necessary packages:

```bash
python3 -m pip install -r requirements.txt
```

Copy the `.env.sample` and replace `{discord-token}` with your bot's Discord token in `.env`

```bash
cp .env.sample .env
```

Copy the `config.json.sample` to `config.json` and Replace the following placeholders

### `{lfg_channel_id}`
ID of the channel to which the bot should listen to the command


## Run
```bash
python3 bot.py
```
