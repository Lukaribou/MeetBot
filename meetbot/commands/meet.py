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

        user = Profile.from_db(ctx.db, ctx.author.id)
        all_p = [Profile(x) for x in ctx.db.execute('SELECT * FROM profiles WHERE active = 1 AND NOT user_id = ?',
                                                    ctx.author.id).fetchall()]
        len_all_p = len(all_p)

        all_p = list(filter(lambda x: (user.age - 10 <= x.age <= user.age + 10), all_p))

        print("%d restants sur %d résultats de base" % (len(all_p), len_all_p))
        for p in all_p:
            print(p)
