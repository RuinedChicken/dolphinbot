import json
import discord
from discord.ext import commands
import random

def setup_commands(bot):

    @bot.command(name='dolphin_help')
    async def custom_help(ctx):
        """
        Provides help. Hopefully.
        """
        # Gather command names and descriptions
        commands_descriptions = [f"!{command.name} - {command.help or 'No description provided'}" for command in bot.commands]
        
        # Join the command descriptions into a single string
        help_message = "\n".join(commands_descriptions)
            
        # Send the help message
        await ctx.send(f"**Available Commands:**\n{help_message}")
        
        # Save to a file in the root directory
        with open("commands_list.txt", "w", encoding="utf-8") as file:
            file.write(help_message)


    @bot.command(name='grozdan')
    async def post_image(ctx):
            """
            Гроздан.
            """
            image_path = 'images/grozdan.png'  # Update the path and filename to your specific image
            try:
                with open(image_path, 'rb') as img:
                    await ctx.send(file=discord.File(img))
            except FileNotFoundError:
                await ctx.send("Image isn't there. Blame Pollo.")


    @bot.command(name='quote')
    async def get_quote(ctx, arg: str):
        """
        Fetches a quote by its ID from the quotes.json file and posts it, or a random quote if 'r' is passed.
        """
        try:
            with open('quotes.json', 'r') as file:
                quotes = json.load(file)
                if arg.lower() == 'r':
                    quote = random.choice(quotes)  # Ensure this selects randomly each time
                else:
                    try:
                        quote_id = int(arg)
                        quote = next((q for q in quotes if q['id'] == quote_id), None)
                        if not quote:
                            await ctx.send("Couldn't find a quote with that ID. Blame Pollo.")  # ID is valid but not found, blame Pollo
                            return
                    except ValueError:
                        await ctx.send("Provide a valid fucking ID or 'r' for a random quote.")  # User's fault for not providing a valid ID
                        return

                # Send the quote
                await ctx.send(f'"{quote["body"]}" - {quote["author"]}')
                
        except FileNotFoundError:
            await ctx.send("The quotes file is missing. Blame Pollo.")  # File missing, blame Pollo
        except json.JSONDecodeError:
            await ctx.send("There's a problem with the quotes file format. Blame Pollo.")  # File format issue, blame Pollo