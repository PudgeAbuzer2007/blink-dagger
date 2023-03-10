import datetime
import discord
import logging

from discord.ext import tasks

TOKEN = BOT_TOKEN
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class YLBotClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hours, self.minutes, self.flag = 0, 0, False
        self.time = None
        self.clock = '⏰'

    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if "help" in message.content.lower():
            await message.channel.send(f'You can set a timer if type "set_timer '
                                       f'in ## hours ## minutes"')
        if 'set_timer' in message.content.lower():
            self.hours = int(message.content.split('in ')[1].split(' hours')[0])
            self.minutes = int(message.content.split('hours ')[1].split(' minutes')[0])
            self.flag = True
            self.time = datetime.datetime.now()
            await message.channel.send(f'The timer should start in {self.hours} hours and {self.minutes} minutes.')
            self.my_background_task.start(id_chan=message.channel.id)

    @tasks.loop(seconds=20)  # task runs every 20 seconds
    async def my_background_task(self, id_chan):
        if self.flag:
            delta = datetime.datetime.now() - self.time
            logger.info(delta)
            if delta.seconds >= self.hours * 3600 + self.minutes * 60:
                self.hours, self.minutes, self.flag = 0, 0, False
                self.time = None
                channel = self.get_channel(id_chan)  # channel ID goes here
                await channel.send(f'{self.clock} Time X has come!')
                self.my_background_task.stop()

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = YLBotClient(intents=intents)
client.run(TOKEN)
# set_timer in 0 hours 1 minutes
