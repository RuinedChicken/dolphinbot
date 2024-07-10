from discord.ext import commands
import discord
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='bot.log', filemode='a')
class AddScore(commands.Cog, name="Add score"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='add_score')
    async def post_image(self, ctx):
        """
        Usage: !add_score map round_number. Also, send a screenshot in the same message 
        """
        try:
            with open(image_path, 'rb') as img:
                await ctx.send(file=discord.File(img))
        except FileNotFoundError:
            await ctx.send("No Гроздан. Blame Pollo.")

    # ------------------------------------------------------------------------------------------------------------------------------------------


async def setup(bot):
    await bot.add_cog(AddScore(bot))
