from log_message import log_message
from discord.ext import tasks, commands
from datetime import datetime, timedelta

class MessagePurger(commands.Cog):
    def __init__(self, config, lfg_channel):
        self.config = config
        self.lfg_channel = lfg_channel
        self.purger.start()

    def cog_unload(self):
        self.purger.cancel()

    @tasks.loop(seconds=60)
    async def purger(self):
        before_datetime = datetime.utcnow() - timedelta(seconds=self.config.get('purge_messages_after'))

        try:
            log_message(self.lfg_channel.guild, f'purging messages from "{self.lfg_channel}#{self.lfg_channel.id}" older than {before_datetime}')
            deleted_messages = await self.lfg_channel.purge(before=before_datetime, limit=100)

        except Exception as e:
            print(e)

        
