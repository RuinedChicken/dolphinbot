from discord.ext import commands

class Utils(commands.Cog, name="Utils"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='dolphin_help')
    async def custom_help(self, ctx):
        """
        Provides help. Hopefully.
        """
        # Gather command names and descriptions
        commands_descriptions = [f"!{command.name} - {command.help or 'No description provided'}" for command in self.bot.commands]
        
        # Join the command descriptions into a single string
        help_message = "\n".join(commands_descriptions)
            
        # Send the help message
        await ctx.send(f"**Available Commands:**\n{help_message}")
        
        # Save to a file in the root directory
        with open("commands_list.txt", "w", encoding="utf-8") as file:
            file.write(help_message)

async def setup(bot):
    await bot.add_cog(Utils(bot))
