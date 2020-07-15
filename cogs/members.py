import discord, datetime, pytz
from discord.ext import commands

class MembersModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #!user <@member>
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name = "user")
    async def user(self, ctx, member:discord.Member = None):
        if member == None:
            member = ctx.author

        name = f"{member.name}#{member.discriminator}"

        if str(member.status) is "dnd":
            status = "do not disturb"
        else:
            status = str(member.status)

        joined = member.joined_at
        joined = joined.replace(microsecond=0)
        joinDate = f"{joined.date()} @ {joined.time()}"

        created = member.created_at
        created = created.replace(microsecond=0)
        createDate = f"{created.date()} @ {created.time()}"

        role = member.top_role
        if role is ctx.guild.default_role:
            role = "None"

        avatarURL = str(member.avatar_url)
        avatarURL = avatarURL[:-15]
        avatarURL = avatarURL + ".jpg"


        embed=discord.Embed(colour=member.colour, timestamp=pytz.utc.localize(datetime.datetime.now(), is_dst=None).astimezone(pytz.timezone('Europe/Istanbul')))
        embed.set_author(icon_url=avatarURL, name=name)
        embed.set_thumbnail(url=avatarURL)
        embed.add_field(name="<:meguGun:534548813923352596>Rank", value=f"{role}", inline=True)
        embed.add_field(name="Status", value=f"{status.capitalize()}", inline=False)
        embed.add_field(name="Join Date", value=f"{joinDate}", inline=False)
        embed.add_field(name="Created At", value=f"{createDate}", inline=False)

        await ctx.channel.send(embed = embed)

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name = "joined")
    async def joined(self, ctx, member:discord.Member = None):
        if member == None:
            member = ctx.message.author
        name = f"{member.name}#{member.discriminator}"

        joined = member.joined_at
        joined = joined.date()
        await ctx.channel.send(f"{name} joined this guild at {joined}.")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name = "created")
    async def created(self, ctx, member:discord.Member = None):
        if member == None:
            member = ctx.message.author
        name = f"{member.name}#{member.discriminator}"

        created = member.created_at
        created = created.date()
        await ctx.channel.send(f"{name} created at {created}.")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name = "avatar")
    async def avatar(self, ctx, member:discord.Member = None):
        if member == None:
            member = ctx.message.author
        name = f"{member.name}#{member.discriminator}"

        imageURL = str(member.avatar_url)
        imageURL = imageURL[:-15]
        imageURL = imageURL + ".jpg"

        embed = discord.Embed(title=name)
        embed.set_image(url=imageURL)

        await ctx.channel.send(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="rank")
    async def rank(self, ctx, member:discord.Member = None):
        if member == None:
            member = ctx.message.author
        name = f"{member.name}#{member.discriminator}"

        role = member.top_role
        if role == ctx.guild.default_role:
            role = "none"
        await ctx.channel.send(f"Rank of {name} is {role}.")

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="permissions")
    async def perm(self, ctx, member:discord.Member = None):
        if ctx.message.author.guild_permissions.administrator:
            if member == None:
                member = ctx.message.author

        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        embed = discord.Embed(title='Permissions for:', description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))

        embed.add_field(name='\uFEFF', value=perms)

        await ctx.channel.send(embed=embed)



def setup(bot):
    bot.add_cog(MembersModule(bot))
