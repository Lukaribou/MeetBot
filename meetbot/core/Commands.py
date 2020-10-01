from typing import Dict, Union
from meetbot.config import OWNER_ID, EMOJIS
import discord


class Context:
    def __init__(self, bot, msg):
        self.bot = bot
        self.msg: discord.Message = msg
        self.msg_args = msg.content[2:].split(" ")
        self.channel: discord.abc.Messageable = msg.channel
        self.author: Union[discord.Member, discord.User] = msg.author


class Command:
    def __init__(self, name: str, function, aliases=None, owner_only=False):
        self.name = name
        self.function = function
        self.aliases = [] if aliases is None else aliases
        self.owner_only = owner_only

    def run(self, ctx: Context):
        if self.owner_only and ctx.author.id != OWNER_ID:
            ctx.channel.send(EMOJIS["x"] + " **This command is reserved for the bot owner**")
        else:
            self.function()


class CommandsManager:
    def __init__(self):
        self.commands: Dict[str, Command] = {}

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

    def add_command(self, fonction, name, aliases=None, owner_only=False):
        """Add the command to self.commands"""
        if self.has_command(name):
            raise Exception(f"Command {name} already defined (or an alias is already attribued)")
        print("coucou")
        self.commands[name] = Command(name, fonction, aliases, owner_only)
