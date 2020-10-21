from meetbot.core.Commands import Command, Context
from meetbot.config import EMOJIS


class FileCommand(Command):
    def __init__(self):
        super().__init__("maintenance", "Set the maintenance mode to the provided value.", "maintenance <on/off>",
                         owner_only=True)

    async def run(self, ctx: Context):
        if not await super().run(ctx):
            return
        await ctx.bot.toggle_maintenance()
        await ctx.channel.send(f"{EMOJIS['ok']} **Maintenance mode {'ON' if ctx.bot.maintenance else 'OFF'}.**")
