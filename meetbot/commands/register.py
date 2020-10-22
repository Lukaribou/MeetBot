import mariadb

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
            return await ctx.channel.send(EMOJIS["x"] + "**You are already registered ! Use `del` command to delete "
                                                        "your actual account.**")
        try:
            ctx.db.execute("INSERT INTO profiles (user_id) VALUES (?)", ctx.author.id)
            await ctx.channel.send(EMOJIS['ok'] + " **You are now registered ! You can use `set` to modify your "
                                                  "informations.**")
        except mariadb.Error as e:
            print("SQL Error occured on register.py : " + str(e))
            await ctx.channel.send(EMOJIS['x'] + " **An error occured. It will be repaired soon.**")
