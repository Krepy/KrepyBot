import discord
from discord.ext import commands
from discord import permissions
import json
import sys, traceback

with open("config.json", "r") as f:
    config = json.load(f)


async def _prefix(bot, message):
    return config["prefix"]


extensions = [
    "cogs.admin",
    "cogs.channels",
    "cogs.error_handler",
    "cogs.manga_database_renew",
    "cogs.megu",
    "cogs.members",
    "cogs.mmanga",
    "cogs.owner",
    "cogs.simple",
]
TOKEN = config["token"]


bot = commands.Bot(
    command_prefix=_prefix,
    status=discord.Status.idle,
    activity=discord.Game(name="Booting..."),
)
bot.remove_command("help")

if __name__ == "__main__":
    for cog in extensions:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print(
                f"Failed to load extension {cog}.",
                file=sys.stderr,
            )
            traceback.print_exc()


@bot.event
async def on_ready():
    print("Ready to go!")
    print(f"Serving: {len(bot.guilds)} guilds.")
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Game(name="with potatoes!!"),
    )


bot.run(TOKEN, bot=True, reconnect=True)
