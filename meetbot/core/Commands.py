import os
import importlib.util
from typing import Dict, Union, List

import discord

from meetbot.config import OWNER_ID, EMOJIS


class Context:
    def __init__(self, bot, msg):
        self.bot = bot
        self.msg: discord.Message = msg
        self.msg_args = msg.content.split(" ")
        self.channel: discord.abc.Messageable = msg.channel
        self.author: Union[discord.Member, discord.User] = msg.author


class Command:
    def __init__(self, name: str, aliases: List[str] = None, owner_only=False):
        self.name = name
        self.aliases = [] if aliases is None else aliases
        self.owner_only = owner_only

    async def run(self, ctx: Context):
        if ctx.bot.debug_mode:
            print(f'Commande {self.name} exécutée !')
        if self.owner_only and ctx.author.id != OWNER_ID:
            await ctx.channel.send(EMOJIS["x"] + " **This command is reserved for the bot owner**")
            return
        else:
            print(EMOJIS["ok"] + f" Commande {self.name} !")


class CommandsManager:
    def __init__(self, bot):
        self.commands: Dict[str, Command] = {}
        self._bot = bot

    def get_command(self, cmd_name):
        """Return the command if it is defined, else None"""
        for x in self.commands.values():
            print(x)
            if cmd_name == x.name or ((x.aliases is not None) and cmd_name in x.aliases):
                return x
        return None

    def has_command(self, cmd_name):
        """Return true if the command exists (check aliases too)"""
        return self.get_command(cmd_name)

    def add_command(self, cmd: Command):
        """Add the command to self.commands"""
        if self._bot.debug_mode:
            print(f'\tCommande {cmd.name} chargée !')
        if self.has_command(cmd.name):
            raise Exception(f"Command {cmd.name} already defined (or an alias is already attribued)")
        self.commands[cmd.name] = cmd

    def add_commands(self, cmds: List[Command]):
        print(f'Chargement de {len(cmds)} commandes.')
        for command in cmds:
            self.add_command(command)

    def load_commands_from_dir(self, do_not_load: List[str] = None):
        do_not_load = [] if do_not_load is None else do_not_load
        cmds = []
        for file in os.listdir('./commands/'):
            if file not in do_not_load:
                # https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
                spec = importlib.util.spec_from_file_location(f'meetbot.commands.{file}', f'./commands/{file}')
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                cmds.append(mod.FileCommand())
        self.add_commands(cmds)
