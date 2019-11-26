import discord
from discord.ext import commands
import random
import requests
from lxml import html
import lxml


class ImageModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.guild_only()
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.command(name='birb', aliases=['bird'])
    async def birb(self, ctx):

        checkSource = requests.get("https://some-random-api.ml/img/birb")
        checkPage = html.fromstring(checkSource.content)


        checkPage2 = lxml.html.tostring(checkPage)
        imgURL = checkPage2[12:-6]
        imgURL = str(imgURL, 'utf-8')


        embed = discord.Embed(title="Birb", url=imgURL, colour=0xE65858)
        embed.set_image(url=imgURL)

        await ctx.channel.send(embed=embed)



def setup(bot):
    bot.add_cog(ImageModule(bot))
