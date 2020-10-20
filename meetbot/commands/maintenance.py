from meetbot.core.Commands import Command, Context


class FileCommand(Command):
    def __init__(self):
        super().__init__("maintenance", "Set the maintenance mode to the provided value.", "maintenance <on/off>",
                         owner_only=True)

    async def run(self, ctx: Context):
        if not await super().run(ctx):
            return
