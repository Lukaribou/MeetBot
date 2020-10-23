from meetbot.core.Commands import Command, Context
from meetbot.config import EMOJIS
from meetbot.utils.Profile import Profile, PROFILE_COLUMS
from meetbot.utils.functions import get_int


class FileCommand(Command):
    def __init__(self):
        super().__init__("set", "Modifies your informations in the database.\n"
                                "Set the value to NULL if you want to reset a field.\n"
                                "Please use english to be more easily found",
                         "set <field> <value>", cooldown=4)

    async def run(self, ctx: Context):
        if not await super().run(ctx):
            return
        if not ctx.db.profile_exist(ctx.author.id):
            return await ctx.channel.send(EMOJIS['x'] + " **You currently don't have a profile. Use `reg` to create "
                                                        "it.**")

        if len(ctx.msg_args) == 2 and ctx.msg_args[1] == 'list':
            return await ctx.channel.send(
                "Here are  all the editable fields: `" + '`, `'.join(PROFILE_COLUMS.keys()) + "`")
        if len(ctx.msg_args) < 3:
            return await ctx.channel.send(EMOJIS['x'] + " **Usage: `set <field> <value>`. Enter `set list` to display "
                                                        "editable fields.**")
        if ctx.msg_args[1] not in PROFILE_COLUMS.keys():
            return await ctx.channel.send(EMOJIS['x'] + " **This field is undefined or not editable. Use `set list` to "
                                                        "display editable fields.**")

        if ctx.msg_args[1] in ['age', 'color'] and ctx.msg_args[2].upper() != 'NULL':
            try:
                new_value = get_int(ctx.msg_args[2])
                if ctx.msg_args[1] == 'age' and (0 > new_value or new_value > 99):
                    return await ctx.channel.send(EMOJIS['x'] + ' **Age field need to be `between 0 and 100`.**')
                elif ctx.msg_args[1] == 'color' and (0 > new_value or new_value > 16777215):
                    return await ctx.channel.send(EMOJIS['x'] +
                                                  ' **Color field need to be `between 0 and 16777215 (0xFFFFFF)`.**')
            except ValueError:
                return await ctx.channel.send(EMOJIS['x'] + ' **Age or color field are `number`.'
                                                            'Color is in `hexadecimal`.**')
        elif ctx.msg_args[2].upper() == 'NULL':
            new_value = 0 if ctx.msg_args[1] in ['age', 'color'] else ''
        else:
            new_value = ' '.join(ctx.msg_args[2:])
            if len(new_value) > PROFILE_COLUMS[ctx.msg_args[1]]:
                return await ctx.channel.send(EMOJIS['x'] + f' **The `{ctx.msg_args[1]}` field is limited to'
                                                            f'`{PROFILE_COLUMS[ctx.msg_args[1]]}` characters and you'
                                                            f'have written `{len(new_value)}`.'
                                                            f'You can try to `use English` to reduce the length.**')
        ctx.db.execute(f"UPDATE profiles SET {ctx.msg_args[1]} = ? WHERE user_id = ?", new_value, ctx.author.id)
        await ctx.channel.send(f'{EMOJIS["ok"]} **`{ctx.msg_args[1]}` field has now the value `{new_value}`**')
