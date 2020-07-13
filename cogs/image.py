import discord
from discord.ext import commands
import random
import httpx
from lxml import html
import os

class ImageModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='birb')
    async def birb(self, ctx):

        checkSource = httpx.get("https://some-random-api.ml/img/birb")
        checkPage = html.fromstring(checkSource.content)


        checkPage2 = html.tostring(checkPage)
        imgURL = checkPage2[12:-6]
        imgURL = str(imgURL, 'utf-8')


        embed = discord.Embed(title="Birb", url=imgURL, colour=0xE65858)
        embed.set_image(url=imgURL)

        await ctx.channel.send(embed=embed)

    @commands.guild_only()
    #@commands.cooldown(2, 5, commands.BucketType.user)
    @commands.command(name='bird')
    async def bird(self, ctx):

        randomFile=random.choice(os.listdir("Bird/"))

        f = discord.File(f"Bird/{randomFile}", filename=randomFile)

        e = discord.Embed(title="Bird", colour=0x64C6E9)
        e.set_image(url=f"attachment://{randomFile}")
        await ctx.channel.send(embed=e, file=f)


def setup(bot):
    bot.add_cog(ImageModule(bot))
