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
            target = Profile(ctx.db, target.id) if ctx.db.profile_exist(target.id) else None

        if target is None or not target:
            await ctx.channel.send(EMOJIS['x'] + ' **The provided id/user does not match any profile.**')

        em = discord.embeds.Embed(color=target.color, title='In')
