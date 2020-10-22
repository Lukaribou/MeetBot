import sys

from meetbot.core.MeetBot import MeetBot
from meetbot.config import TOKEN


if __name__ == '__main__':
    mods = sys.argv[1:]

    bot = MeetBot(debug_mode='-d' in mods, maintenance_mode='-m' in mods)

    bot.cmds.load_commands_from_dir(do_not_load=['__pycache__'])

    bot.run(TOKEN)
