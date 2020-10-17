import os
import importlib.util

from typing import List

from meetbot.core.Commands import Command
from meetbot.core.MeetBot import MeetBot
from meetbot.config import TOKEN


def load_commands() -> List[Command]:
    cmds = []
    for file in os.listdir('./commands/'):
        if not file == '__pycache__':
            # https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
            spec = importlib.util.spec_from_file_location(f'meetbot.commands.{file}', f'./commands/{file}')
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            cmds.append(mod.FileCommand())

    return cmds


if __name__ == '__main__':
    bot = MeetBot()

    bot.cmds.add_commands(load_commands())

    bot.run(TOKEN)
