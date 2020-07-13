import discord, httpx
from discord.ext import commands, tasks
from lxml import html


class MangaDatabaseRenewModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.updateMangaDatabase.start()

    @tasks.loop(hours=1)
    async def updateMangaDatabase(self):
        await self.dbUpdate()

    async def dbUpdate(self):
        a = 1
        d = 1
        c = 1

        source = httpx.get("https://mavimanga.com/manga-listesi")
        page = html.fromstring(source.content)
        totalP = (page.xpath("//div[@class='navigation']/ul/li[1]/span/text()"))[0]
        totalP = totalP.split(" - ")
        totalP = int(totalP[1])

        print("Started DB renewal.")

        while a <= totalP:
            source = httpx.get("https://mavimanga.com/manga-listesi/sayfa/" + str(a))
            page = html.fromstring(source.content)
            post = page.xpath("//ul[@class='manga-list']/li/a/@href")

            for b in post:
                await self.updateMMangaInfo(b)
                c+=1

            print("Getting page " + str(a) + " of " + str(totalP) + " is done.")
            a=a+1

    async def updateMMangaInfo(self, link):
        sourceS = httpx.get(link)
        pageS = html.fromstring(sourceS.content)

        try:
            title = ((pageS.xpath(f"//meta[@property='og:title']/@content"))[0].split(" – "))[0]
        except:
            title = "No Title"

        try:
            imgURL=(pageS.xpath(f"//meta[@property='og:image']/@content"))[0]
        except:
            imgURL = "https://i.resimyukle.xyz/1yx268.png"

        durum=(pageS.xpath(f"//span[@class='mangasc-stat']/text()"))[0]
        mangaka=(pageS.xpath(f"//td[./b/text()='Mangaka:']/text()"))[0]
        bolum=(pageS.xpath("//td[./b/text()='Bölüm Sayısı:']/text()"))[0]
        turler=", ".join(str(x) for x in pageS.xpath("//td[./b/text()='Türler:']/ul/li/a/text()"))
        diger=(pageS.xpath("//td[./b/text()='Diğer Adları:']/text()"))[0]
        cikis=(pageS.xpath("//td[./b/text()='Çıkış Yılı:']/text()"))[0]
        try:
            konu=(pageS.xpath("//meta[@property='og:description']/@content"))[0]
        except:
            konu = " "

        try:
            latestL=(pageS.xpath("(//a[@class='mangaep-episode'])[1]/@href"))[0]
            latestN=(pageS.xpath("(//a[@class='mangaep-episode'])[1]/text()"))[0]
        except:
            latestN="Bölüm Yok"
            latestL=link

        manga = await self.bot.pg_con.fetch(f'SELECT * FROM manga WHERE name = $1', title)
        if not manga:
           await self.bot.pg_con.execute(f'INSERT INTO manga (name, author, "releaseDate", status, genre, konu, "latestN", "latestL", url, img, total, alias) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)', title, mangaka, cikis, durum, turler, konu, latestN, latestL, link, imgURL, bolum, diger)
        else:
           await self.bot.pg_con.execute(f'UPDATE manga SET author = $2, "releaseDate" = $3, status = $4, genre = $5, konu = $6, "latestN" = $7, "latestL" = $8, url = $9, img = $10, total = $11, alias = $12 WHERE name = $1', title, mangaka, cikis, durum, turler, konu, latestN, latestL, link, imgURL, bolum, diger)

    @commands.is_owner()
    @commands.command(name='mdatabaserenew', aliases=['dbrenew'])
    async def mangaDatabaseRenew(self, ctx):

        await self.dbUpdate()
        await ctx.channel.send("Database renewing is done.\n")

def setup(bot):
    bot.add_cog(MangaDatabaseRenewModule(bot))
