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
        C_ALL_P = [Profile(x) for x in ctx.db.execute('SELECT * FROM profiles WHERE active = 1 AND NOT user_id = ?',
                                                      ctx.author.id).fetchall()]

        all_p = C_ALL_P.copy()

        for i in range(5, 40, 5):  # age +- [5, 10, 15, ...]
            all_p = list(filter(lambda x: (user.age - i <= x.age <= user.age + i), C_ALL_P))
            if len(all_p) > 0:
                break

        if len(all_p) == 0:
            return await ctx.channel.send(EMOJIS['x'] + " **It seems that no profile matches yours. I'll send you "
                                                        "the first profile I find...**",
                                          embed=await C_ALL_P[0].to_embed(ctx.bot))

        all_p = sorted(all_p, key=lambda x: x.last_meet, reverse=True)  # trier last_meet récent => ancien



        print("%d restants sur %d résultats de base" % (len(all_p), len(C_ALL_P)))
        for p in all_p:
            print(p)
