import discord
import os
import match_fetcher
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='GetMatchAbove',
             help='Gets live matches with ELO above the input')
async def get_match_above(ctx, min_elo: int):
    live_matches = match_fetcher.get_live_matches(min_elo)
    response = random.choice(live_matches)
    await ctx.send(response)

@bot.command(name='GetMatchBelow',
             help='Gets live matches with ELO below the input ')
async def get_match_below(ctx, max_elo: int):
    live_matches = match_fetcher.get_live_matches(0, max_elo)
    response = random.choice(live_matches)
    await ctx.send(response)

@bot.command(name='GetMatchBetween',
             help='Gets live matches with ELO in the input range')
async def get_match_between(ctx, min_elo: int, max_elo: int):
    live_matches = match_fetcher.get_live_matches(min_elo, max_elo)
    response = random.choice(live_matches)
    await ctx.send(response)


bot.run(TOKEN)
