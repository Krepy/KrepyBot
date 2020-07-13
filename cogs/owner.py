from discord.ext import commands
import json


class OwnerModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.is_owner()
    @commands.command(name='setPrefix')
    async def setPrefix(self, ctx, newPref):
        with open('config.json', 'r') as f:
            config = json.load(f)
        config['prefix'] = newPref
        with open('config.json', 'w') as f:
            json.dump(config, f)
        await ctx.channel.send("Prefix set.")
        self.bot.command_prefix = newPref


    @commands.is_owner()
    @commands.command(name='load', hidden=True)
    async def load(self, ctx, *, cog: str):

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')


    @commands.is_owner()
    @commands.command(name='unload', hidden=True)
    async def unload(self, ctx, *, cog: str):

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')


    @commands.is_owner()
    @commands.command(name='reload', hidden=True)
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
