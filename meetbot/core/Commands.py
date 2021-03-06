import importlib.util
import os
import threading
from typing import Dict, Union, List

import discord

from meetbot.config import OWNER_ID, EMOJIS
from .DataBase import DataBase


class Context:
    def __init__(self, bot, msg):
        self.bot = bot
        self.msg: discord.Message = msg
        self.msg_args = msg.content.split(" ")
        self.channel: discord.abc.Messageable = msg.channel
        self.author: Union[discord.Member, discord.User] = msg.author
        self.db: DataBase = bot.db


class Command:
    def __init__(self, name: str, description: str, use: str = None, aliases: List[str] = None, owner_only=False,
                 cooldown=1):
        """Create a new command\n
        cooldown is in ms"""
        self.name = name
        self.description = description
        self.use = name if use is None else use
        self.aliases = [] if aliases is None else aliases
        self.owner_only = owner_only
        self.cooldown = cooldown

    async def run(self, ctx: Context) -> bool:
        """Execute the command (override this method)\n
        Return true if the overrided method is ok to be executed."""
        if self.owner_only and ctx.author.id != OWNER_ID:
            m = await ctx.channel.send(EMOJIS["x"] + " **This command is reserved to the bot owner**")
            await m.delete(delay=5)
            return False
        if ctx.bot.debug_mode:
            print(f'Commande {self.name} exécutée !')
        return True


class CommandsManager:
    def __init__(self, bot):
        self.commands: Dict[str, Command] = {}
        self._bot = bot
        self._cooldown: Dict[str, List[str]] = {}

    def get_command(self, cmd_name):
        """Return the command if it is defined, else None"""
        for x in self.commands.values():
            if cmd_name == x.name or ((x.aliases is not None) and cmd_name in x.aliases):
                return x
        return None

    def has_command(self, cmd_name):
        """Return true if the command exists (check aliases too)"""
        return self.get_command(cmd_name)

    def add_command(self, cmd: Command):
        """Add the command to self.commands"""
        if self._bot.debug_mode:
            print(f'\tCommande "{cmd.name}" chargée !')
        if self.has_command(cmd.name):
            raise Exception(f"Command {cmd.name} already defined (or an alias is already attribued)")
        self.commands[cmd.name] = cmd

    def add_commands(self, cmds: List[Command]):
        """Add all the commands to self.commands, using self.add_command() for each"""
        print(f'Chargement de {len(cmds)} commandes:')
        for command in cmds:
            self.add_command(command)

    def load_commands_from_dir(self, do_not_load: List[str] = None):
        """Load all the commands from ./commands/ (assuming the file is containing a FileCommand class)"""
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

    def is_in_cooldown(self, author: discord.User, cmd: str):
        """Return true if the user is in the cooldown for this cooldown"""
        return (author.id in self._cooldown.keys()) and (cmd in self._cooldown.get(author.id))

    def add_in_cooldown(self, author: discord.User, cmd: Command):
        """Add the command to the user cooldown"""
        if author.id in self._cooldown.keys():
            self._cooldown[author.id].append(cmd.name)
        else:
            self._cooldown[author.id] = [cmd.name]
        threading.Timer(cmd.cooldown, self.delete_of_cooldown, [author, cmd.name]).start()

    def delete_of_cooldown(self, author: discord.User, cmd: str):
        """Delete the command from the user's cooldown"""
        if author.id in self._cooldown.keys():
            if len(self._cooldown.get(author.id)) == 1:
                self._cooldown.pop(author.id)
            else:
                self._cooldown.get(author.id).remove(cmd)
