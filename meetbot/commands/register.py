from meetbot.core.Commands import Command, Context
from meetbot.config import EMOJIS


class FileCommand(Command):
    def __init__(self):
        super().__init__(
            "register",
            "Registers you in the database.\nAfter that, you can use the `set` command to modify your informations.",
            aliases=["reg", "new"], cooldown=5)

    async def run(self, ctx: Context):
        if not await super().run(ctx):
            return
        if ctx.db.profile_exist(ctx.author.id):
            return ctx.channel.send(EMOJIS["x"] + "You are already registered ! Use `del` command to delete your "
                                                  "actual account.")
        print("c'est cool")
