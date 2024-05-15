"""What do you think bot.py does, pylint?!"""

# bot.py
import asyncio
import logging
import discord
from discord.ext import commands
from private import TOKEN


async def main():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')
        print('------')

    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')

    # Load cogs
    await bot.load_extension("ImagePostingCog")
    await bot.load_extension("QuoteCog")
    await bot.load_extension("SoundboardCog")
    await bot.load_extension("UtilsCog")

    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
