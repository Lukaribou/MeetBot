import discord

import meetbot.config as config
from meetbot.core.Commands import *
from meetbot.core.DataBase import DataBase


class MeetBot(discord.Client):
    def __init__(self, run_now=False, debug_mode=True, maintenance_mode=False, **options):
        super().__init__(**options)
        self.prefix = config.PREFIX
        self.owner_id = config.OWNER_ID
        self.debug_mode = debug_mode
        self.cmds = CommandsManager(self)
        self.maintenance = maintenance_mode
        self.db = DataBase(config.DB_HOST, config.DB_PORT, "meetbot")

        if run_now:
            self.run(config.TOKEN)

    async def toggle_maintenance(self):
        """Toggle the maintenance mode"""
        self.maintenance = not self.maintenance
        print("TOGGLE MAINTENANCE MODE TO : " + str(self.maintenance))
        await self.on_ready()

    async def on_ready(self):
        if self.maintenance:
            await self.change_presence(
                activity=discord.Activity(name='in maintenance', type=0),
                status='idle'
            )
            print(f'Logged as {self.user} in maintenance mode.')
        else:
            await self.change_presence(
                activity=discord.Activity(name=f'for {EMOJIS["heart"]}', type=3))
            print(f'Logged as {self.user}')

    async def on_message(self, message: discord.Message):
        if not message.content.startswith(self.prefix) or message.content == config.PREFIX \
                or message.author.bot or (self.maintenance and message.author.id != OWNER_ID):
            return
        message.content = message.content[len(self.prefix):]
        cmd = self.cmds.get_command(message.content.split(" ")[0])

        if self.cmds.is_in_cooldown(message.author, cmd.name) and message.author.id != OWNER_ID:
            m = await message.channel.send(f'{EMOJIS["x"]} **This command has a cooldown of {cmd.cooldown}s !**')
            await m.delete(delay=5)
        else:
            self.cmds.add_in_cooldown(message.author, cmd)
            await cmd.run(Context(self, message))
