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
            return await ctx.channel.send(EMOJIS['x'] + ' **You need a profile to use this command.**')

        all_p = [Profile(x) for x in ctx.db.execute('SELECT * FROM profiles WHERE active = 1 AND NOT user_id = ?',
                                                    ctx.author.id).fetchall()]

        print(all_p)
