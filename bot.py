"""What do you think bot.py does, pylint?!"""

import discord
from discord.ext import commands
from bot_commands import setup_commands
from private import TOKEN


intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------')

setup_commands(bot)

bot.run(TOKEN)
