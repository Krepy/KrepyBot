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
        latestU = await self.bot.pg_con.fetchrow(f'SELECT latest FROM "latestUpdate"')
        print(latestU)
        if not latestU['latest']:
            latestUpdate = datetime.datetime.now() + datetime.timedelta(days=-1, hours=-5)
        else:
            latestUpdate = datetime.datetime.strptime(latestU['latest'], '%Y-%m-%d %H:%M:%S')

        feedChannels = await self.bot.pg_con.fetch(f'SELECT "channelID" FROM "feed"')
        if not feedChannels:
            return


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

                manga = await self.bot.pg_con.fetchrow(f'SELECT * FROM manga WHERE url=$1', mangaInfoURL)

                sendString = f"{manga['name']} "

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

                for channelR in feedChannels:
                    channelID = channelR['channelID']
                    roleID = await self.bot.pg_con.fetchrow(f'SELECT "RoleID" FROM "mmRoles" WHERE "channelID"=$1 AND "mangaURL"=$2', str(channelID), mangaURL)
                    if roleID:
                        print(str(roleID))
                        print(type(roleID))
                        sendString = f"<@&{roleID['RoleID']}>\n" + sendString

                    channel = self.bot.get_channel(int(channelID))
                    await channel.send(sendString)

                i += 1

        dateOfEntry = datetime.datetime.strptime(nFeed.entries[0].updated, '%Y-%m-%dT%H:%M:%S+00:00') + datetime.timedelta(seconds=1)


        await self.bot.pg_con.fetchrow(f'UPDATE "latestUpdate" SET latest=$1', str(dateOfEntry))


    @commands.is_owner()
    @commands.guild_only()
    @commands.command(name='setMMFeed', aliases=['setMM'])
    async def setMMFeed(self, ctx):
        channelID = str(ctx.channel.id)
        feedChannel = await self.bot.pg_con.fetchrow(f'SELECT * FROM feed WHERE "channelID"=$1', channelID)
        if feedChannel:
            await ctx.channel.send("Feed already set in this channel.")
        else:
            await self.bot.pg_con.execute(f'INSERT INTO feed ("channelID") VALUES ($1)', channelID)
            await ctx.channel.send("Feed set.")

    @commands.is_owner()
    @commands.guild_only()
    @commands.command(name='delMMFeed', aliases=['delMM'])
    async def delMMFeed(self, ctx):
        channelID = str(ctx.channel.id)
        feedChannel = await self.bot.pg_con.fetch(f'SELECT * FROM feed WHERE "channelID"=$1', channelID)
        if feedChannel:
            await self.bot.pg_con.execute(f'DELETE FROM feed WHERE "channelID"=$1', channelID)
            await ctx.channel.send("Channel deleted from feed list.")
        else:
            await ctx.channel.send("This channel is not in feed list.")

    @commands.is_owner()
    @commands.guild_only()
    @commands.command(name='addToFeedDict')
    async def addToFeedDict(self, ctx, mangaURL, role:discord.Role = None):
        if role:
            if mangaURL:
                try:
                    mangaURL = ((mangaURL.split('/manga/'))[1].split('/'))[0]
                except:
                    pass

                roleID = str(role.id)
                channelID = str(ctx.channel.id)

                check = await self.bot.pg_con.fetch(f'SELECT "RoleID" FROM "mmRoles" WHERE "channelID"=$1 AND "mangaURL"=$2', channelID, mangaURL)
                if check:
                    if check == roleID:
                        await ctx.channel.send("Entry is already in the dict.")
                    else:
                        await self.bot.pg_con.execute(f'UPDATE "mmRoles" SET "RoleID"=$1 WHERE "channelID"=$2 AND "mangaURL"=$3', roleID, channelID, mangaURL)
                        await ctx.channel.send("Entry updated.")
                else:
                    await self.bot.pg_con.execute(f'INSERT INTO "mmRoles" ("channelID", "mangaURL", "RoleID") VALUES ($1, $2, $3)', channelID, mangaURL, roleID)
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

            roleID = str(role.id)
            channelID = str(ctx.channel.id)

            check = await self.bot.pg_con.fetch(f'SELECT "RoleID" FROM "mmRoles" WHERE "channelID"=$1 AND "mangaURL"=$2', channelID, mangaURL)
            if check:
                await self.bot.pg_con.execute(f'DELETE FROM "mmRoles" WHERE "channelID"=$2 AND "mangaURL"=$3', channelID, mangaURL)
                await ctx.channel.send("Entry deleted.")
            else:
                await ctx.channel.send("Entry is not in the dictionary.")

        else:
            await ctx.channel.send("You did not specify a manga's url.")




def setup(bot):
    bot.add_cog(FeedModule(bot))
