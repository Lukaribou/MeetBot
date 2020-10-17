import time

import discord.embeds

from meetbot.core.Commands import Command, Context


class FileCommand(Command):
    def __init__(self):
        super().__init__("ping")

    async def run(self, ctx: Context):
        em = discord.embeds.Embed(color=0x00FF00)
        t1 = time.time()
        m = await ctx.channel.send(embed=discord.embeds.Embed(color=0xFF0000))
        em.add_field(
            name='Latence API:',
            value=str((time.time() - t1) * 1000).split('.')[0] + 'ms')
        await m.edit(embed=em)
