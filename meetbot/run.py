import os
import importlib.util

from typing import List

from meetbot.core.Commands import Command
from meetbot.core.MeetBot import MeetBot
from meetbot.config import TOKEN


if __name__ == '__main__':
    bot = MeetBot(debug_mode=True)

    bot.cmds.load_commands_from_dir(do_not_load=['__pycache__'])

    bot.run(TOKEN)
