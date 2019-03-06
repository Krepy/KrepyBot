import discord, sqlite3
from discord.ext import commands
import random
import requests
from lxml import html

class MmangaModule(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    #@commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='srcdb', aliases=['mmdb'])
    async def mangaSearch(self, ctx, *, mName: str):

        mName = mName + " – Mavi Manga"
        sqlite_file = 'manga_db.sqlite'
        tn = 'manga'
        cn1 = 'name'

        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()

        c.execute(f'SELECT * FROM {tn} WHERE {cn1}=?', [mName])
        all = c.fetchall()
        allA = all[0]

        title=allA[0]
        mangaka=allA[1]
        cikis=allA[2]
        durum=allA[3]
        turlerS=allA[4]
        konu=allA[5]
        latestN=allA[6]
        latestL=allA[7]
        post=allA[8]
        imgURL=allA[9]
        bolum=allA[10]
        diger=allA[11]

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

        conn.close()

    @commands.command(name='mmanga', aliases=['mavimanga'])
    async def mSearch(self, ctx, *, mname):
        mname = mname.replace(" ", "-")

        post = "https://mavimanga.com/manga/" + mname
        source = requests.get(post)

        page = html.fromstring(source.content)

        title=random.choice(page.xpath(f"//meta[@property='og:title']/@content"))

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


def setup(bot):
    bot.add_cog(MmangaModule(bot))
