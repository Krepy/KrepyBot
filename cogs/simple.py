import discord
from discord.ext import commands

class SimpleModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #!ping
    @commands.command(name="ping")
    async def ping(self, ctx):
        ping_ = self.bot.latency
        ping = round(ping_ * 1000)
        await ctx.channel.send(f"My ping is {ping} ms.")

    @commands.command(name="repeat", aliases=["afterme"])
    async def repeat(self, ctx, *, string: str):
        await ctx.channel.send(string)


def setup(bot):
    bot.add_cog(SimpleModule(bot))
