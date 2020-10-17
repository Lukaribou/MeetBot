import meetbot.config as config
from meetbot.core.Commands import *
import discord


class MeetBot(discord.Client):
    def __init__(self, run_now=False, debug_mode=True, **options):
        super().__init__(**options)
        self.prefix = config.PREFIX
        self.owner_id = config.OWNER_ID
        self.debug_mode = debug_mode
        self.cmds = CommandsManager(self)

        if run_now:
            self.run(config.TOKEN)

    async def on_ready(self):
        print(f'Logged as {self.user}')

    async def on_message(self, message: discord.Message):
        if (not message.content.startswith(self.prefix)) or message.author.bot:
            return
        message.content = message.content[len(self.prefix):]
        await self.cmds.get_command(message.content.split(" ")[0]).run(Context(self, message))
