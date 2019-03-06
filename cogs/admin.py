import discord
from discord.ext import commands
from discord import permissions

class AdminModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="ban")
    async def ban(self, ctx, member:discord.Member = None, *, reason = None):
        if ctx.message.author.guild_permissions.ban_members:
            if member == None and name != None:
                member = ctx.message.guild.get_member_named(name)
                if name == None:
                    await ctx.channel.send("You need to type a valid name.")
                    return
            if member == None:
                await ctx.channel.send("You need mention a member to ban.")
                return
            if member == ctx.message.author:
                await ctx.channel.send("You cannot ban yourself.")
                return
            if ctx.message.author.top_role <= member.top_role:
                await ctx.channel.send("You cannot ban someone that has higher or equal rank to you.")
                return
            if reason == None:
                reason = "no reason at all!!"
            message = f"You have been banned from {ctx.guild.name} for {reason}!"
            await member.send(message)
            await ctx.guild.ban(member)
            await ctx.channel.send(f"{member} is banned!")
        else:
            await ctx.channel.send("You dont have permissions to ban a member.")


    @commands.command(name="kick")
    async def kick(self, ctx, member:discord.Member = None, *,reason = None):
        if ctx.message.author.guild_permissions.kick_members:
            if member == None and name != None:
                member = ctx.message.guild.get_member_named(name)
                if name == None:
                    await ctx.channel.send("You need to type a valid name.")
                    return
            if member == None:
                await ctx.channel.send("You need mention a member to kick.")
                return
            if member == ctx.message.author:
                await ctx.channel.send("You cannot kick yourself.")
                return
            if ctx.message.author.top_role <= member.top_role:
                await ctx.channel.send("You cannot kick someone that has higher or equal rank to you.")
                return
            if reason == None:
                reason = "no reason at all!!"
            message = f"You have been kicked from {ctx.guild.name} for {reason}!"
            await member.send(message)
            await ctx.guild.kick(member)
            await ctx.channel.send(f"{member} is kicked!")
        else:
            await ctx.channel.send("You dont have permissions to kick a member!")


def setup(bot):
    bot.add_cog(AdminModule(bot))
