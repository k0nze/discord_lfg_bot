from datetime import datetime

def log_message(guild, message):
    datetime_now = datetime.now()
    print(str(datetime_now) + " - " + f'{guild.name}#{guild.id}: {message}')
