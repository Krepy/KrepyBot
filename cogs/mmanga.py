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

        mName = mName + " – Mavi Manga"
        sqlite_file = 'manga_db.sqlite'
        tn = 'manga'
        cn1 = 'name'

        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()

        c.execute(f'SELECT * FROM {tn} WHERE {cn1}=?', (mName,))
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

    @commands.command(name='dbupdate', aliases=['update'])
    async def dbUpdate(self, ctx, *, mName):

        mName2 = mName + " – Mavi Manga"
        sqlite_file = 'manga_db.sqlite'
        url = "https://mavimanga.com/manga/" + mName

        source = requests.get(url)
        pageS = html.fromstring(source.content)

        tn = "manga"
        cn1 = "name"
        cn2 = "author"
        cn3 = "releaseDate"
        cn4 = "status"
        cn5 = "genre"
        cn6 = "desc"
        cn7 = "latestN"
        cn8 = "latestL"
        cn9 = "url"
        cn10 = "img"
        cn11 = "total"
        cn12 = "alias"
        ct = 'TEXT'

        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()

        c.execute(f'SELECT * FROM {tn} WHERE {cn1}=?', (mName2,))
        all = c.fetchall()

        if not all:

            title = random.choice(
                pageS.xpath(
                    f"//meta[@property='og:title']/@content"
                )
            )

            if title.startswith("Sayfa Bulunamadı"):
                await ctx.channel.send("Aradığınız mangaya ulaşılamadı, lütfen başka bir isim seçin. <:lul:536833872076210198>")
            else:
                imgURL = pageS.xpath(
                    f"//meta[@property='og:image']/@content"
                )
                if imgURL:
                    imgURL = imgURL[0]
                else:
                    imgURL = "https://i.resimyukle.xyz/1yx268.png"

                if not title:
                    title = "No Title"
                durum = random.choice(
                    pageS.xpath(
                        f"//span[@class='mangasc-stat']/text()"
                    )
                )
                mangaka = random.choice(
                    pageS.xpath(
                        f"//td[./b/text()='Mangaka:']/text()"
                    )
                )
                bolum = random.choice(
                    pageS.xpath(
                        "//td[./b/text()='Bölüm Sayısı:']/text()"
                    )
                )
                turler = pageS.xpath(
                    "//td[./b/text()='Türler:']/ul/li/a/text()"
                )
                turlerS = ", ".join(str(x) for x in turler)

                diger = random.choice(
                    pageS.xpath(
                        "//td[./b/text()='Diğer Adları:']/text()"
                    )
                )
                cikis = random.choice(
                    pageS.xpath(
                        "//td[./b/text()='Çıkış Yılı:']/text()"
                    )
                )
                konu = random.choice(
                    pageS.xpath(
                        "//meta[@property='og:description']/@content"
                    )
                )

                latestL = pageS.xpath(
                    "(//a[@class='mangaep-episode'])[1]/@href"
                )

                if latestL:
                    latestL = random.choice(latestL)
                    latestN = pageS.xpath(
                        "(//a[@class='mangaep-episode'])[1]/text()"
                    )
                    latestN = latestN[0]
                else:
                    latestN = "Bölüm Yok"
                    latestL = b

                c.execute(
                    f"INSERT OR IGNORE INTO {tn} ({cn1}, {cn2}, {cn3}, {cn4}, {cn5}, {cn6}, {cn7}, {cn8}, {cn9}, {cn10}, {cn11}, {cn12}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        title,
                        mangaka,
                        cikis,
                        durum,
                        turlerS,
                        konu,
                        latestN,
                        latestL,
                        url,
                        imgURL,
                        bolum,
                        diger,
                    ),
                )
        else:
            latestL = pageS.xpath(
                "(//a[@class='mangaep-episode'])[1]/@href"
            )

            if latestL:
                latestL = random.choice(latestL)
                latestN = pageS.xpath(
                    "(//a[@class='mangaep-episode'])[1]/text()"
                )
                latestN = latestN[0]
            else:
                latestN = "Bölüm Yok"
                latestL = mName2

            c.execute(f'UPDATE {tn} SET {cn7}=? , {cn8}=? WHERE {cn1}=?', (latestN, latestL, mName2))

        conn.commit()

        c.execute(f'SELECT * FROM {tn} WHERE {cn1}=?', (mName2,))
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


def setup(bot):
    bot.add_cog(MmangaModule(bot))
