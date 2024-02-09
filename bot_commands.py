"""Commands for the bot."""

import asyncio
from discord.ext import commands
import os
import json
import random
import discord



def setup_commands(bot):
    """
    Giga function with all commands
    """
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
        image_path = 'images/grozdan.png'
        try:
            with open(image_path, 'rb') as img:
                await ctx.send(file=discord.File(img))
        except FileNotFoundError:
            await ctx.send("Image isn't there. Blame Pollo.")


    @bot.command(name='quote')
    async def get_quote(ctx, arg: str):
        """
        Displays a quote. Usage: !quote number for specific quote, !quote r for random quote.
        """
        # Fetches a quote by its ID from the quotes.json file and posts it, or a random quote if 'r' is passed.
        try:
            with open('quotes.json', 'r', encoding="utf-8") as file:
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

    @bot.command(name='addquote')
    async def add_quote(ctx, *, text: str):
        """
        Adds a new quote. Usage: !addquote "quote text" - Author
        """
        # The filename where quotes are stored, assumed to be in the same directory as the bot script.
        filename = 'quotes.json'

        # Attempt to split the text into quote and author.
        try:
            body, author = map(str.strip, text.rsplit(" - ", 1))
        except ValueError:
            # If splitting fails, send an error message.
            await ctx.send("Use the format: \"quote text\" - Author")
            return

        # Continue with adding the quote to the file.
        try:
            # Load existing quotes with UTF-8 encoding
            with open(filename, 'r', encoding='utf-8') as file:
                quotes = json.load(file)
            
            # Determine the next available ID
            if quotes:  # Check if the list is not empty
                last_id = quotes[-1]['id']  # Get the ID of the last quote in the list
                next_id = last_id + 1
            else:
                next_id = 1  # Start from ID 1 if the list is empty
            
            # Create the new quote
            new_quote = {
                'id': next_id,
                'body': body,
                'author': author
            }
            
            # Add the new quote to the list
            quotes.append(new_quote)
            
            # Write the updated list back to the file
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(quotes, file, ensure_ascii=False, indent=4)  # Use ensure_ascii=False to write UTF-8 characters directly
            
            # Send confirmation message
            await ctx.send(f"Quote added successfully with ID {next_id}.")
        
        except FileNotFoundError:
            await ctx.send("The quotes file is missing. Blame Pollo.")
        except json.JSONDecodeError:
            await ctx.send("There's a problem with the quotes file format. Blame Pollo.")
        except Exception as e:
            # Handle other unexpected exceptions
            await ctx.send(f"An unexpected error occurred: {e}")
