from discord.ext import commands
import discord
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='bot.log', filemode='a')
class ImagePosting(commands.Cog, name="Image posting"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='grozdan')
    async def post_image(self, ctx):
        """
        Гроздан.
        """
        image_path = 'images/grozdan.png'
        try:
            with open(image_path, 'rb') as img:
                await ctx.send(file=discord.File(img))
        except FileNotFoundError:
            await ctx.send("No Гроздан. Blame Pollo.")
    # ------------------------------------------------------------------------------------------------------------------------------------------

    
async def setup(bot):
    await bot.add_cog(ImagePosting(bot))
