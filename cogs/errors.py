import discord
import sys
import traceback
from discord.ext import commands
import datetime
from difflib import get_close_matches

class CommandErrorHandler(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog and cog._get_overridden_method(cog.cog_command_error) is not None:
            return
        ignored = (commands.NotOwner)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CommandNotFound):
            cmd = ctx.invoked_with
            cmds = [cmd.name for cmd in self.client.commands if not cmd.hidden] 
            matches = get_close_matches(cmd, cmds)
            if len(matches) > 0:
                await ctx.send(f'Command "{cmd}" not found, maybe you meant "{matches[0]}"?')
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass
        
        elif isinstance(error,commands.MemberNotFound):
            await ctx.send("Sorry, that member was not found. Make sure you have provided a valid user id/user name.")

        elif isinstance(error,commands.BadArgument):
            await ctx.send(f"{error.message}")

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(error)

        elif isinstance(error,commands.CommandOnCooldown):
            message=f"This command is on cooldown. Please try again after {datetime.timedelta(seconds=round(error.retry_after))} seconds."
            await ctx.send(message)  
                  
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(client):
    client.add_cog(CommandErrorHandler(client))