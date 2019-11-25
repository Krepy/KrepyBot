from discord.ext import commands
import json


class OwnerModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setPrefix')
    @commands.is_owner()
    async def setPrefix(self, ctx, newPref):
        with open('config.json', 'r') as f:
            configs = json.load(f)
        configs['prefix'] = newPref
        with open('config.json', 'w') as f:
            json.dump(configs, f)
        await ctx.channel.send("Prefix set.")
        self.bot.command_prefix = newPref

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')


def setup(bot):
    bot.add_cog(OwnerModule(bot))
