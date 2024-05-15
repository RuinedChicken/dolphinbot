from discord.ext import commands
import discord
import os

class Soundboard(commands.Cog, name="Soundboard"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='play')
    async def play(self, ctx, sound_clip: str):
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

        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        # If the bot is not connected to a voice channel, join vc
        if not voice_client or not voice_client.is_connected():
            channel = ctx.author.voice.channel
            voice_client = await channel.connect()

        # Play the audio if not already playing something
        if not voice_client.is_playing():
            voice_client.play(discord.FFmpegPCMAudio(executable='ffmpeg/bin/ffmpeg.exe', source=sound_clip_path))  # Adjust FFmpeg path as needed
            # await ctx.send(f"Now playing: {sound_clip}")

    # ------------------------------------------------------------------------------------------------------------------------------------------
    @commands.command(name='leave')
    async def leave(self, ctx):
        """What do you _think_ it does."""
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("Silly Dolphin, I'm not in a voice channel. If I am, blame Pollo.")     

    # ------------------------------------------------------------------------------------------------------------------------------------------
    @commands.command(name='cliplist')
    async def list_sounds(self, ctx):
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

async def setup(bot):
    await bot.add_cog(Soundboard(bot))
