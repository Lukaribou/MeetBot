import discord

from meetbot.core.Commands import Command, Context
from meetbot.config import EMOJIS, VERSION, PREFIX


class FileCommand(Command):
    def __init__(self):
        super().__init__("help", "Provides help about one command or all the commands",
                         "help <command_name/nothing>", ["?", "h"], cooldown=2)

    async def run(self, ctx: Context):
        if not await super().run(ctx):
            return

        if len(ctx.msg_args) == 2:
            cmd = ctx.bot.cmds.get_command(ctx.msg_args[1])
            if cmd is None:
                await ctx.channel.send(f'{EMOJIS["x"]} **The command `{ctx.msg_args[1]}` does not exist.**')
            else:
                em = discord.embeds.Embed(color=0x00FF00, title=f'Help for the {cmd.name} command')
                em.set_thumbnail(url='https://static.thenounproject.com/png/67363-200.png')
                em.add_field(name='Description:', value=cmd.description)
                em.add_field(name='Use:', value=PREFIX + cmd.use)
                em.add_field(name='Aliases ?',
                             value=('`' + "`, `".join(cmd.aliases) + '`') if len(cmd.aliases) != 0 else EMOJIS['x'])
                em.add_field(name='Owner only ?', value=EMOJIS['ok'] if cmd.owner_only else EMOJIS['x'])
                em.add_field(name='Cooldown:', value=str(cmd.cooldown) + 's')
                await ctx.channel.send(embed=em)
        else:
            em = discord.embeds.Embed(color=0x00FF00, title='MeetBot list of commands',
                                      description="To get more informations about a command, use :\n`help "
                                                  "<command_name>`.")
            em.set_thumbnail(url='https://static.thenounproject.com/png/67363-200.png')
            em.set_footer(text=EMOJIS['lock'] + ' : Bot owner only | Version : ' + VERSION)

            # TODO: len(bot.cmds.commands) > 25 => crash

            for c in ctx.bot.cmds.commands.values():
                em.add_field(
                    name=c.name + (f' ({EMOJIS["lock"]})' if c.owner_only else ''),
                    value=c.description)

            await ctx.channel.send(embed=em)
