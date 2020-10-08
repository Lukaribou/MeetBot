import meetbot.config as config
from meetbot.core.Commands import *


class MeetBot(discord.Client):
    def __init__(self, run_now=False, **options):
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
        message.content = message.content[2:]
        await self.cmds.get_command("test").run(Context(self, message))


if __name__ == '__main__':
    bot = MeetBot()


    async def test(ctx: Context):
        await ctx.channel.send("coucou")


    bot.cmds.add_command(test, 'test')
    bot.run(config.TOKEN)
