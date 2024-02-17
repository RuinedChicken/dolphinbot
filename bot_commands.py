"""Commands for the bot."""

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
            await ctx.send("No Гроздан. Blame Pollo.")

    # ---------------------------------------- QUOTES ---------------------------------------- 
            
    @bot.command(name='quotelist')
    async def get_quotelist(ctx):
        """Displays a list of all available quote IDs and missing quote IDs."""
        try:
            with open('quotes.json', 'r', encoding="utf-8") as file:
                quotes = json.load(file)
                # Extracting quote IDs and sorting them
                quote_ids = sorted([quote["id"] for quote in quotes])

                if quote_ids:
                    # Initialize variables
                    ranges, missing = [], []
                    start = end = quote_ids[0]

                    # Find ranges of available IDs
                    for qid in quote_ids[1:]:
                        if qid == end + 1:
                            end = qid
                        else:
                            ranges.append(f"{start}-{end}")
                            start = end = qid
                    
                    # Add the final range
                    ranges.append(f"{start}-{end}" if start != end else f"{start}")

                    # Find missing IDs
                    full_range = set(range(1, quote_ids[-1] + 1))
                    missing_ids = full_range - set(quote_ids)
                    for mid in sorted(missing_ids):
                        if not missing or mid != missing[-1][-1] + 1:
                            missing.append([mid])
                        else:
                            missing[-1].append(mid)

                    # Format missing ranges
                    missing_ranges = [f"{m[0]}-{m[-1]}" if len(m) > 1 else str(m[0]) for m in missing]

                    # Format the message
                    message = "Available Quote IDs:\n" + ", ".join(ranges)
                    if missing_ranges:
                        message += "\n\nMissing Quote IDs:\n" + ", ".join(missing_ranges)
                else:
                    message = "No quotes available."
        except FileNotFoundError:
            message = "The quotes file is missing. Blame Pollo."
        except json.JSONDecodeError:
            message = "There's a problem with the quotes file format. Blame Pollo."

        await ctx.send(message)

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
                            await ctx.send("Couldn't find a quote with that ID.")  # ID is valid but not found, blame Pollo
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
        Adds a new quote. Usage: !addquote quote text - Author
        """

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

    # ---------------------------------------- SOUNDBOARD ---------------------------------------- 
            
    @bot.command(name='play')
    async def play(ctx, sound_clip: str):
        """Will attempt to join your vc and play a sound clip. Can keep on playing until you tell it to go w !leave"""
        soundboard_folder = 'soundboard'
        sound_extensions = ['.mp3', '.wav', '.ogg']  # List of supported audio file extensions

        # Is the user in vc?
        if ctx.author.voice is None:
            await ctx.send("Join a voice channel first. If you are in vc, blame Pollo.")
            return

        # Find the full path with extension
        sound_clip_path = None
        for ext in sound_extensions:
            potential_path = os.path.join(soundboard_folder, sound_clip + ext)
            if os.path.exists(potential_path):
                sound_clip_path = potential_path
                break

        if not sound_clip_path:
            await ctx.send("Sound clip not found.")
            return

        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

        # If the bot is not connected to a voice channel, join vc
        if not voice_client or not voice_client.is_connected():
            channel = ctx.author.voice.channel
            voice_client = await channel.connect()

        # Play the audio if not already playing something
        if not voice_client.is_playing():
            voice_client.play(discord.FFmpegPCMAudio(executable='ffmpeg/bin/ffmpeg.exe', source=sound_clip_path))  # Adjust FFmpeg path as needed
            await ctx.send(f"Now playing: {sound_clip}")

    @bot.command(name='leave')
    async def leave(ctx):
        """What do you _think_ it does."""
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("Silly Dolphin, I'm not in a voice channel. If I am, blame Pollo.")        

    @bot.command(name='cliplist')
    async def list_sounds(ctx):
        """Lists all available sound clips."""
        soundboard_folder = 'soundboard'
        sound_extensions = ['.mp3', '.wav', '.ogg']
        available_sounds = []

        # List all files in the soundboard folder and filter by supported extensions
        for file in os.listdir(soundboard_folder):
            if any(file.endswith(ext) for ext in sound_extensions):
                # Remove the file extension
                sound_name, _ = os.path.splitext(file)
                available_sounds.append(sound_name)

        if available_sounds:
            message = "Available sounds:\n" + "\n".join(available_sounds)
        else:
            message = "No sounds found in the soundboard folder. Definitely blame Pollo."

        await ctx.send(message)