from meetbot.core.Commands import Command, Context
from meetbot.config import EMOJIS
from meetbot.utils.Profile import Profile


class FileCommand(Command):
    def __init__(self):
        super().__init__("set", "Modifies your informations in the database.\n"
                                "Set the value to NULL if you want to reset a field.\n"
                                "Please use english to be more easily found",
                         "set <field> <value>", cooldown=4)

    async def run(self, ctx: Context):
        if not await super().run(ctx):
            return
        if not ctx.db.profile_exist(ctx.author.id):
            return await ctx.channel.send(EMOJIS['x'] + " **You currently don't have a profile. Use `reg` to create "
                                                        "it.**")

        profile = Profile(ctx.db, ctx.author.id)

        if len(ctx.msg_args) == 2 and ctx.msg_args[1] == 'list':
            return await ctx.channel.send(
                "Here are  all the editable fields: `" + '`, `'.join(profile.get_editable_columns_names()) + "`")
        if len(ctx.msg_args) < 3:
            return await ctx.channel.send(EMOJIS['x'] + " **Usage: `set <field> <value>`. Enter `set list` to display "
                                                        "editable fields.**")
        if ctx.msg_args not in profile.get_editable_columns_names():
            return await ctx.channel.send(EMOJIS['x'] + " **This field is undefined or not editable. Use `set list` to "
                                                        "display editable fields.**")

        new_value = None

        if ctx.msg_args[1] == 'age' and ctx.msg_args[2] != 'NULL':
            try:
                new_value = int(ctx.msg_args[2])
            except ValueError:
                return await ctx.channel.send(EMOJIS['x'] + ' You need to set your age with a number.')
