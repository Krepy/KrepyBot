import discord, sys, traceback, asyncpg, json
from discord.ext import commands, tasks
from discord import permissions
from itertools import cycle

with open("config.json", "r") as f:
    config = json.load(f)

async def _prefix(bot, message):
    return config['prefix']

async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(database=config['dbDatabase'], user=config['dbUsername'], password=config['dbPassword'], host=config['dbHost'])

extensions = [
    "cogs.image",
    "cogs.admin",
    "cogs.channels",
    "cogs.error_handler",
    "cogs.manga_database_renew",
    "cogs.megu",
    "cogs.members",
    "cogs.mmanga",
    "cogs.owner",
    "cogs.simple",
    "cogs.feed",
]
TOKEN = config['token']


bot = commands.Bot(
    command_prefix=_prefix,
    status=discord.Status.idle,
    activity=discord.Game(name="Booting..."),
)
bot.remove_command("help")

def loadCogs():
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
    loadCogs()

bot.loop.run_until_complete(create_db_pool())
bot.run(TOKEN, bot=True, reconnect=True)
