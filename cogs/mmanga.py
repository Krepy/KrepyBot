import discord, sqlite3
from discord.ext import commands
import random
import requests
from lxml import html

class MmangaModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='mmanga', aliases=['mavimanga'])
    async def mSearch(self, ctx, *, mname):
        mname = mname.replace(" ", "-")

        post = "https://mavimanga.com/manga/" + mname
        source = requests.get(post)

        page = html.fromstring(source.content)

        title=random.choice(page.xpath(f"//meta[@property='og:title']/@content"))
        title=title[:-13]

        if not title.startswith('Sayfa bulunamadı'):
            imgURL=page.xpath(f"//meta[@property='og:image']/@content")
            if imgURL:
                imgURL = imgURL[0]
            else:
                imgURL = "https://i.resimyukle.xyz/1yx268.png"
            durum=random.choice(page.xpath(f"//span[@class='mangasc-stat']/text()"))
            mangaka=random.choice(page.xpath(f"//td[./b/text()='Mangaka:']/text()"))
            bolum=random.choice(page.xpath("//td[./b/text()='Bölüm Sayısı:']/text()"))
            turler=page.xpath("//td[./b/text()='Türler:']/ul/li/a/text()")
            turlerS=", ".join(str(x) for x in turler)

            diger=random.choice(page.xpath("//td[./b/text()='Diğer Adları:']/text()"))
            cikis=random.choice(page.xpath("//td[./b/text()='Çıkış Yılı:']/text()"))
            konu=random.choice(page.xpath("//meta[@property='og:description']/@content"))

            latestL=page.xpath("(//a[@class='mangaep-episode'])[1]/@href")

            if latestL:
                latestL=random.choice(latestL)
                latestN=page.xpath("(//a[@class='mangaep-episode'])[1]/text()")
                latestN = latestN[0]
            else:
                latestN="Bölüm Yok"
                latestL=b


            embed = discord.Embed(title=f'__**{title}**__', url=post, colour=0x64C6E9)
            embed.set_thumbnail(url=imgURL)
            embed.add_field(name='Türler', value=turlerS, inline=False)
            embed.add_field(name='Diğer Adlar', value=diger)
            embed.add_field(name='Çıkış Yılı', value=cikis, inline=True)
            embed.add_field(name='Mangaka', value=mangaka)
            embed.add_field(name='Toplam Bölüm', value=bolum)
            embed.add_field(name='Durum', value=durum)
            embed.add_field(name='Son Bölüm', value=f'[{latestN}]({latestL})', inline=True)
            embed.add_field(name='Konusu', value=konu)
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("Aradığınız mangaya ulaşılamadı, lütfen başka bir isim seçin. <:lul:536833872076210198>")

    #@commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='srcdb', aliases=['mmdb'])
    async def mangaSearch(self, ctx, *, mName: str):

        manga = await self.bot.pg_con.fetchrow(f'SELECT * FROM manga WHERE name=$1', mName)

        title=manga['name']
        mangaka=manga['author']
        cikis=manga['releaseDate']
        durum=manga['status']
        turlerS=manga['genre']
        konu=manga['konu']
        latestN=manga['latestN']
        latestL=manga['latestL']
        post=manga['url']
        imgURL=manga['img']
        bolum=manga['total']
        diger=manga['alias']

        embed = discord.Embed(title=f'__**{title}**__', url=post, colour=0x64C6E9)
        embed.set_thumbnail(url=imgURL)
        embed.add_field(name='Türler', value=turlerS, inline=False)
        embed.add_field(name='Diğer Adlar', value=diger)
        embed.add_field(name='Çıkış Yılı', value=cikis, inline=True)
        embed.add_field(name='Mangaka', value=mangaka)
        embed.add_field(name='Toplam Bölüm', value=bolum)
        embed.add_field(name='Durum', value=durum)
        embed.add_field(name='Son Bölüm', value=f'[{latestN}]({latestL})', inline=True)
        embed.add_field(name='Konusu', value=konu)
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(MmangaModule(bot))
