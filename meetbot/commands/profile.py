import discord

from meetbot.core.Commands import Command, Context
from meetbot.config import EMOJIS
from meetbot.utils.Profile import Profile


class FileCommand(Command):
    def __init__(self):
        super().__init__("profile", "Displays the profile of the provided person.", "profile <id/mention/me>",
                         ['p'], cooldown=4)

    async def run(self, ctx: Context):
        if not await super().run(ctx):
            return

        target = None
        if len(ctx.msg_args) == 1 or ctx.msg_args[2] == 'me':
            target = ctx.author
        elif len(ctx.msg.mentions) != 0:
            target = ctx.msg.mentions[0]
        else:
            try:
                target = ctx.bot.get_user(int(ctx.msg_args[1]))
            except ValueError:
                pass

        if target is not None:
            target = Profile.from_db(ctx.db, target.id) if ctx.db.profile_exist(target.id) else None

        if target is None or not target:
            return await ctx.channel.send(EMOJIS['x'] + ' **The provided id/user does not match any profile.**')
        if not target.active:
            return await ctx.channel.send(EMOJIS['x'] + ' **This profile is not active.**')

        user: discord.User = ctx.bot.get_user(target.user_id)

        def t(a):
            if type(a) is str:
                return a if a is not '' else 'Not provided'
            else:
                return a if a is not 0 else 'Not provided'

        em = discord.embeds.Embed(color=target.color)
        em.set_author(name='Informations about: ' + user.name, icon_url=user.avatar_url)
        em.add_field(name='Name:', value=t(target.name))
        em.add_field(name='Gender:', value=t(target.gender))
        em.add_field(name='Age:', value=str(t(target.age)))
        em.add_field(name='Description:', value=t(target.description))
        em.add_field(name='Country:', value=t(target.country))
        em.add_field(name='Profile creation date:', value=str(target.creation_date))
        em.add_field(name='Last meet command:', value=str(target.creation_date))
        em.add_field(name='Other:', value=t(target.other))
        em.set_footer(text='User id: ' + str(target.user_id))

        await ctx.channel.send(embed=em)
