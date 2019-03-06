import discord
from discord.ext import commands
import sqlite3
import random
import requests
from lxml import html

class MangaDatabaseRenewModule(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name='mdatabaserenew', aliases=['dbrenew'])
    async def mangaDatabaseRenew(self, ctx):
        sqlite_file = 'manga_db.sqlite'
        tn = 'manga'
        cn1 = 'name'
        cn2 = 'author'
        cn3 = 'releaseDate'
        cn4 = 'status'
        cn5 = 'genre'
        cn6 = 'desc'
        cn7 = 'latestN'
        cn8 = 'latestL'
        cn9 = 'url'
        cn10 = 'img'
        cn11 = 'total'
        cn12 = 'alias'
        ct = 'TEXT'

        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()

        c.execute(f'DELETE FROM {tn}')

        #XPATH
        a = 1
        d = 1

        source = requests.get("https://mavimanga.com/manga-listesi")
        page = html.fromstring(source.content)
        totalP = random.choice(page.xpath("//div[@class='navigation']/ul/li[1]/span/text()"))
        totalP = totalP.split(" - ")
        totalP = int(totalP[1])


        while a <= totalP:
            source = requests.get("https://mavimanga.com/manga-listesi/sayfa/" + str(a))

            page = html.fromstring(source.content)
            post = page.xpath("//ul[@class='manga-list']/li/a/@href")

            for b in post:
                sourceS = requests.get(b)
                pageS = html.fromstring(sourceS.content)

                imgURL=pageS.xpath(f"//meta[@property='og:image']/@content")
                if imgURL:
                    imgURL = imgURL[0]
                else:
                    imgURL = "https://i.resimyukle.xyz/1yx268.png"
                title=random.choice(pageS.xpath(f"//meta[@property='og:title']/@content"))
                if not title:
                    title = "No Title"
                durum=random.choice(pageS.xpath(f"//span[@class='mangasc-stat']/text()"))
                mangaka=random.choice(pageS.xpath(f"//td[./b/text()='Mangaka:']/text()"))
                bolum=random.choice(pageS.xpath("//td[./b/text()='Bölüm Sayısı:']/text()"))
                turler=pageS.xpath("//td[./b/text()='Türler:']/ul/li/a/text()")
                turlerS=", ".join(str(x) for x in turler)

                diger=random.choice(pageS.xpath("//td[./b/text()='Diğer Adları:']/text()"))
                cikis=random.choice(pageS.xpath("//td[./b/text()='Çıkış Yılı:']/text()"))
                konu=random.choice(pageS.xpath("//meta[@property='og:description']/@content"))

                latestL=pageS.xpath("(//a[@class='mangaep-episode'])[1]/@href")

                if latestL:
                    latestL=random.choice(latestL)
                    latestN=pageS.xpath("(//a[@class='mangaep-episode'])[1]/text()")
                    latestN = latestN[0]
                else:
                    latestN="Bölüm Yok"
                    latestL=b

                c.execute(f'INSERT OR IGNORE INTO {tn} ({cn1}, {cn2}, {cn3}, {cn4}, {cn5}, {cn6}, {cn7}, {cn8}, {cn9}, {cn10}, {cn11}, {cn12}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (title, mangaka, cikis, durum, turlerS, konu, latestN, latestL, b, imgURL, bolum, diger))
            await ctx.channel.send("Getting page " + str(a) + " of " + str(totalP) + " is done.\n")
            a=a+1

        conn.commit()
        conn.close()

def setup(bot):
    bot.add_cog(MangaDatabaseRenewModule(bot))
