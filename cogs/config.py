import imp
from discord.ext import commands
def setup(bot):
    bot.add_cog(Config(bot))

class Config(commands.Cog):
    """Configuration settings for the bot"""
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(brief="Shutdown the bot")
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shutdown the bot"""
        await ctx.send(":wave:")
        await self.bot.close()

    @commands.command(brief="Restart the bot")
    @commands.is_owner()
    async def restart(self, ctx):
        """Restart the bot"""
        await ctx.send(":wave:")
        self.bot.restart = True
        await self.bot.close()
       
    