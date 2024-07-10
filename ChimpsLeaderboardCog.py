from discord.ext import commands
import json
import discord
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='bot.log', filemode='a')
class ChimpsScoring(commands.Cog, name="Chimps scoring"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='add_score')
    async def add_score(self, ctx, map, round):
        """
        Usage: !add_score map round 
        """
        try:
            with open('chimps_scores.json', 'r', encoding="utf-8") as file:
                scores = json.load(file)
                text = ""
                scoresList = scores.get("scores", "putamierda")
                data =  {}
                data["user"]= str(ctx.author.id)
                data["map"]= map
                data["round"]= round
                data["message"] =str(ctx.message.id)
                scoresList.append(data) 
                scores["scores"] = scoresList
                with open('chimps_scores.json', 'w', encoding='utf-8') as file:
                    json.dump(scores, file, ensure_ascii=False, indent=4)  # Use ensure_ascii=False to write UTF-8 characters directly
                await ctx.send("Score saved")
        except FileNotFoundError:
            await ctx.send("No scores file found. Blame Bola")
    @commands.command(name='see_scores')
    async def see_scores(self, ctx):
        """
        Usage: !see_scores 
        """
        try:
            with open('chimps_scores.json', 'r', encoding="utf-8") as file:
                scores = json.load(file)
                text = ""
                scoresList = scores.get("scores", "putamierda")
                for score in scoresList:
                    text = text + "User: " + score["user"]
                    text = text + "Map: " + score["map"]
                    text = text + "Round: " + score["round"]
                    text = text + "Message: " + score["message"]
                await ctx.send(text)
        except FileNotFoundError:
            await ctx.send("No scores file found. Blame Bola")

    

    # ------------------------------------------------------------------------------------------------------------------------------------------


async def setup(bot):
    await bot.add_cog(ChimpsScoring(bot))
