from meetbot.core.Commands import Command, Context
from meetbot.config import EMOJIS
from meetbot.utils.Profile import Profile


class FileCommand(Command):
    def __init__(self):
        super().__init__("meet", "Look for a profile that looks like your.", cooldown=15)

    async def run(self, ctx: Context):
        if not await super().run(ctx):
            return
        if not ctx.db.profile_exist(ctx.author.id):
            await ctx.channel.send(EMOJIS['x'] + ' **You need a profile to use this command.**')
