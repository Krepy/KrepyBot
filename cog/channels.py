import discord
from discord.ext import commands

class CreateModule(commands.cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.guild_only()
    @commands.command(name = "crtText")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def createText(self, ctx, *, name = None):
        guild = ctx.message.guild

        if name == None:
            name = "text_channel"
        elif name != None:
            name = name.lower()
            name = name.replace(" ", "_")

        await guild.create_text_channel(name=name)
        await ctx.channel.send("Channel created.")


    @commands.guild_only()
    @commands.command(name="crtVoice")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def createVoice(self, ctx, *, name = None):
        guild = ctx.message.guild
        if name == None:
            name = "Voice Channel"

        await guild.create_voice_channel(name=name)
        await ctx.channel.send("Channel created.")


    @commands.guild_only()
    @commands.command(name="crtCategory")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def createCategory(self, ctx, *, name = None):
        guild = ctx.message.guild
        if name == None:
            name = "Category"

        await guild.create_category_channel(name=name)
        await ctx.channel.send("Category created.")


    @commands.guild_only()
    @commands.command(name="dltText")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def deleteText(self, ctx, *, chName):
        guild = ctx.guild
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel):
                if channel.name == chName:
                    await channel.delete()
                    return await ctx.channel.send("Channel deleted.")
        return await ctx.channel.send(f'There is no text channels named "{chName}".')


    @commands.guild_only()
    @commands.command(name='dltVoice')
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def deleteVoice(self, ctx, *, chName):
        guild = ctx.guild
        for channel in guild.channels:
            if isinstance(channel, discord.VoiceChannel):
                if channel.name == chName:
                    await channel.delete()
                    return await ctx.channel.send("Channel deleted.")
        return await ctx.channel.send(f'There is no voice channels named "{chName}".')


    @commands.guild_only()
    @commands.command(name='dltCategory')
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def deleteCategory(self, ctx, *, chName):
        guild = ctx.guild
        for channel in guild.channels:
            if isinstance(channel, discord.CategoryChannel):
                if channel.name == chName:
                    await channel.delete()
                    return await ctx.channel.send("Category deleted.")
        return await ctx.channel.send(f'There is no categories named "{chName}".')


    @commands.guild_only()
    @commands.command(name='moveText')
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def moveText(self, ctx, name, *, categoryN):
        guild = ctx.guild
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel) and channel.name == name:
                for category in guild.channels:
                    if isinstance(category, discord.CategoryChannel) and category.name == categoryN:
                        return await channel.edit(category=category, sync_permissions=True)
                    else:
                        category = None
                if category is None:
                    return await ctx.channel.send(f"'{categoryN}' is not a valid category.")
            else:
                channel = None
        if channel is None:
            await ctx.channel.send(f"'{name}' is not a valid text channel.")


    @commands.guild_only()
    @commands.command(name='moveVoice')
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def moveVoice(self, ctx, name, *, categoryN):
        guild = ctx.guild
        for channel in guild.channels:
            if isinstance(channel, discord.VoiceChannel) and channel.name == name:
                for category in guild.channels:
                    if isinstance(category, discord.CategoryChannel) and category.name == categoryN:
                        return await channel.edit(category=category, sync_permissions=True)
                    else:
                        category = None
                if category is None:
                    return await ctx.channel.send(f"'{categoryN}' is not a valid category.")
            else:
                channel = None
        if channel is None:
            await ctx.channel.send(f"'{name}' is not a valid voice channel.")



def setup(bot):
    bot.add_cog(CreateModule(bot))
