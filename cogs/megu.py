import discord
from discord.ext import commands
import random
from lxml import html


class MeguModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #!megu
    @commands.guild_only()
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.command(name='megu', aliases=['megumin', 'meguş'])
    async def megu(self, ctx):
        #siteList = ["https://safebooru.org/index.php?page=dapi&s=post&q=index&tags=megumin", "https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=megumin+rating%3Asafe"]
        checkSource = httpx.get("https://safebooru.org/index.php?page=dapi&s=post&q=index&tags=megumin")
        checkPage = html.fromstring(checkSource.content)
        totalPost = int(random.choice(checkPage.xpath('//posts/@count')))
        totalPage = int(totalPost / 100)

        randomPage = str(random.randint(0, totalPage))
        source = httpx.get("https://safebooru.org/index.php?page=dapi&s=post&q=index&tags=megumin&pid=" + randomPage)
        page = html.fromstring(source.content)
        title = page.xpath('//post/@file_url')


        imgUrl = random.choice(title)
        embed = discord.Embed(title="Megu", description="Explosion magic is the best magic!!", url=imgUrl, colour=0xE65858)
        embed.set_image(url=imgUrl)

        await ctx.channel.send(embed=embed)



def setup(bot):
    bot.add_cog(MeguModule(bot))
