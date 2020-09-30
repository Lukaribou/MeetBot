import discord
import meetbot.config as config
from meetbot.core.Commands import *


class MeetBot(discord.Client):
    def __init__(self, run_now=True, **options):
        super().__init__(**options)
        self.prefix = config.PREFIX
        self.owner_id = config.OWNER_ID
        self.cmds = CommandsManager()

        if run_now:
            self.run(config.TOKEN)

    async def on_ready(self):
        print(f'Logged as {self.user}')

    async def on_message(self, message: discord.Message):
        if (not message.content.startswith(self.prefix)) or message.author.bot:
            return
        self.cmds.get_command("test").run(Context(self, message))


bot = MeetBot()


@bot.cmds.add_command(name='test')
def test(ctx: Context):
    ctx.channel.send("coucou")
