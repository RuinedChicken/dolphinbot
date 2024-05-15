from discord.ext import commands
import discord
import logging
import os

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
    @commands.command(name='e')
    async def emote(self, ctx, emote_name: str):
        """
        Usage: !e file_name (no extension)
        [Laughs in no nitro].
        """
        image_folder = 'images/emotes'
        supported_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp']

        # Find the full path with extension
        emote_path = None
        for ext in supported_extensions:
            potential_path = os.path.join(image_folder, emote_name + ext)
            if os.path.exists(potential_path):
                emote_path = potential_path
                break

        if not emote_path:
            await ctx.send("Emote not found. Blame Pollo.")
            return

        try:
            with open(emote_path, 'rb') as img:
                await ctx.send(file=discord.File(img))
        except FileNotFoundError:
            await ctx.send("Error loading the emote. Blame Pollo.")

    # ------------------------------------------------------------------------------------------------------------------------------------------
    @commands.command(name='list_emotes')
    async def list_emotes(self, ctx):
        """
        Lists all available emote images.
        """
        emotes_folder = 'images/emotes'
        emote_files = os.listdir(emotes_folder)
        emote_files = [f for f in emote_files if os.path.isfile(os.path.join(emotes_folder, f))]

        if not emote_files:
            await ctx.send("No emotes found. Blame Pollo.")
            return

        # Create the message with the list of filenames
        emote_list_message = "Available emotes:\n" + "\n".join(emote_files)

        # Send the message with the list of filenames
        await ctx.send(emote_list_message)

        # # Send the image showing all emotes
        # image_path = 'images/emotes/all_emotes.png'
        # try:
        #     with open(image_path, 'rb') as img:
        #         await ctx.send(file=discord.File(img))
        # except FileNotFoundError:
        #     await ctx.send("The combined emote image is missing. Blame Pollo.")



async def setup(bot):
    await bot.add_cog(ImagePosting(bot))
