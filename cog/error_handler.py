import traceback
import sys
from discord import ext
from discord.ext import commands
import discord

class CommandErrorHandler(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.UserInputError)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.channel.send(f'"{ctx.command}" has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'"{ctx.command}" can not be used in Private Messages.')
            except:
                pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                return await ctx.channel.send('I could not find that member. Please try again.')

        elif isinstance(error, commands.NotOwner):
            return await ctx.channel.send("You are not the owner of the bot.")

        elif isinstance(error, commands.MissingPermissions):
            missing = error.missing_perms

            missing = ["• " + perm for perm in missing]
            missing = [perm.replace("_", " ") for perm in missing]
            missing = [perm.title() for perm in missing]
            missings = '\n'.join(perm for perm in missing)

            return await ctx.channel.send(f"You are missing permissions:\n```{missings}```")

        elif isinstance(error, commands.BotMissingPermissions):
            missing = error.missing_perms

            missing = ["• " + perm for perm in missing]
            missing = [perm.replace("_", " ") for perm in missing]
            missing = [perm.title() for perm in missing]
            missings = '\n'.join(perm for perm in missing)

            return await ctx.channel.send(f"I am missing permissions:\n```{missings}```")



        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
