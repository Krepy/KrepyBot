import discord, feedparser, ast, datetime
from discord.ext import commands, tasks

class FeedModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.feedPush.start()

    @tasks.loop(minutes=5)
    async def feedPush(self):
        await self.mmfeed()

    async def mmfeed(self):
        f = open("Dict/mFeedChannels.txt", "r")
        feedChannels = ast.literal_eval(f.read())
        f.close()

        if not feedChannels:
            return

        f = open("Dict/mFeed.txt", "r")
        feedDict = ast.literal_eval(f.read())
        f.close()

        f = open("Dict/latestUpdate.txt", "r")
        latestUpdate = f.read()
        f.close()

        if not latestUpdate:
            latestUpdate = datetime.datetime.now() + datetime.timedelta(days=-1, hours=-5)
        else:
            latestUpdate = datetime.datetime.strptime(latestUpdate, '%Y-%m-%d %H:%M:%S')


        nFeed = feedparser.parse("https://www.mavimanga.com/r/feed")
        i = 0



        list = []
        while True:
            passU = True

            try:
                entry = nFeed.entries[i]
            except:
                break

            if latestUpdate > datetime.datetime.strptime(entry.updated, '%Y-%m-%dT%H:%M:%S+00:00'):
                break

            for item in list:
                if entry.id == item:
                    passU = False
                    i += 1
                    break

            if passU:
                idSplit = (entry.id.split('/manga/'))[1].split('/')
                mangaURL = idSplit[0]
                mangaEP = int(idSplit[1])

                mangaInfoURL = f'https://mavimanga.com/manga/{mangaURL}/'

                try:
                    roleID = feedDict[f'{mangaURL}']
                except:
                    roleID = None

                manga = await self.bot.pg_con.fetchrow(f'SELECT * FROM manga WHERE url=$1', mangaInfoURL)

                sendString = ""
                if roleID:
                    sendString += f"<@&{roleID}>\n"

                sendString += f"{manga['name']} "

                y = i+1
                count = 0
                while True:
                    a = (nFeed.entries[y].id.split('/manga/'))[1].split('/')
                    if latestUpdate < datetime.datetime.strptime(nFeed.entries[y].updated, '%Y-%m-%dT%H:%M:%S+00:00'):
                        if mangaURL == a[0]:
                            count += 1
                            list.append(nFeed.entries[y].id)
                        y += 1
                    else:
                        break

                if count > 0:
                    sendString += f"{mangaEP-count}-{mangaEP}. bölümler"
                else:
                    sendString += f"{mangaEP}. bölüm"

                sendString += f" eklenmiştir, iyi okumalar. <:yey:733098265784090767> \n{mangaInfoURL}"

                for i in feedChannels:
                    channel = self.bot.get_channel(i)
                    await channel.send(sendString)

                i += 1

        dateOfEntry = datetime.datetime.strptime(nFeed.entries[0].updated, '%Y-%m-%dT%H:%M:%S+00:00') + datetime.timedelta(seconds=1)

        f = open("Dict/latestUpdate.txt", "w")
        f.write(str(dateOfEntry))
        f.close()

    @commands.is_owner()
    @commands.guild_only()
    @commands.command(name='setMMFeed', aliases=['setMM'])
    async def setMMFeed(self, ctx):
        f = open("Dict/mFeedChannels.txt", "r")
        feedChannels = ast.literal_eval(f.read())
        f.close()

        feedChannels.append(ctx.channel.id)

        f = open("Dict/mFeedChannels.txt", "w")
        f.write(str(feedChannels))
        f.close()

        await ctx.channel.send("Feed set.")

    @commands.is_owner()
    @commands.guild_only()
    @commands.command(name='delMMFeed', aliases=['delMM'])
    async def delMMFeed(self, ctx):
        f = open("Dict/mFeedChannels.txt", "r")
        feedChannels = ast.literal_eval(f.read())
        f.close()

        try:
            feedChannels.remove(Integer.valueOf(ctx.channel.id))
        except:
            await ctx.channel.send("This channel is not in the feed channels list.")

        f = open("Dict/mFeedChannels.txt", "w")
        f.write(str(feedChannels))
        f.close()

        await ctx.channel.send("Feed set.")

    @commands.is_owner()
    @commands.guild_only()
    @commands.command(name='addToFeedDict')
    async def addToFeedDict(self, ctx, mangaURL, role:discord.Role = None):
        if role:
            if mangaURL:
                try:
                    mangaURL = (mangaURL.split('/manga/'))[1]
                except:
                    pass

                f = open("Dict/mFeed.txt", "r")
                dict = ast.literal_eval(f.read())
                f.close()

                dict[f'{mangaURL}'] = f'{role.id}'

                f = open("Dict/mFeed.txt", "w")
                f.write(str(dict))
                f.close()

                await ctx.channel.send("Entry added to the dictionary.")

            else:
                await ctx.channel.send("You did not specify a manga's url.")
        else:
            await ctx.channel.send("You did not specify a role.")

    @commands.is_owner()
    @commands.guild_only()
    @commands.command(name='delFromFeedDict')
    async def delFromFeedDict(self, ctx, mangaURL):
        if mangaURL:
            try:
                mangaURL = (mangaURL.split('/manga/'))[1]
            except:
                pass

            f = open("Dict/mFeed.txt", "r")
            dict = ast.literal_eval(f.read())
            f.close()

            try:
                del dict[f'{mangaURL}']
            except:
                await ctx.channel.send("Url is not part of the feed dict.")

            f = open("Dict/mFeed.txt", "w")
            f.write(str(dict))
            f.close()

            await ctx.channel.send("Entry deleted from the dictionary.")

        else:
            await ctx.channel.send("You did not specify a manga's url.")




def setup(bot):
    bot.add_cog(FeedModule(bot))
