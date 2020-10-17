from meetbot.core.Commands import Command, Context


class FileCommand(Command):
    def __init__(self):
        super().__init__("ping")

    async def run(self, ctx: Context):
        await ctx.channel.send("pong")
