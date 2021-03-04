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
             help='Gets live matches with ELO above the input. Usage: !GetMatchAbove [RATING_FLOOR]')
async def get_match_above(ctx, min_elo: int):
    live_matches = match_fetcher.get_live_matches(min_elo)
    if not live_matches:
        await ctx.send("Couldn't find any matches above {}".format(min_elo))
    else:
        response = random.choice(live_matches)
        await ctx.send(response)

@bot.command(name='GetMatchBelow',
             help='Gets live matches with ELO below the input. Usage: !GetMatchBelow [RATING_CEILING]')
async def get_match_below(ctx, max_elo: int):
    live_matches = match_fetcher.get_live_matches(0, max_elo)
    if not live_matches:
        await ctx.send("Couldn't find any matches below {}".format(max_elo))
    else:
        response = random.choice(live_matches)
        await ctx.send(response)

@bot.command(name='GetMatchBetween',
             help='Gets live matches with ELO in the input range. Usage: !GetMatchBetween [RATING_FLOOR] [RATING_CEILING]')
async def get_match_between(ctx, min_elo: int, max_elo: int):
    real_min_elo = min(min_elo, max_elo)
    real_max_elo = max(min_elo, max_elo)

    live_matches = match_fetcher.get_live_matches(real_min_elo, real_max_elo)
    if not live_matches:
        await ctx.send("Couldn't find any matches between {} and {}".format(real_min_elo, real_max_elo))
    else:
        response = random.choice(live_matches)
        await ctx.send(response)

@bot.command(name='GetMatch',
             help='Gets live matches without any elo constraints. Usage: !GetMatch')
async def get_match_between(ctx):
    live_matches = match_fetcher.get_live_matches()
    if not live_matches:
        await ctx.send("Couldn't find any matches ... Is AoE2 down?")
    response = random.choice(live_matches)
    await ctx.send(response)


bot.run(TOKEN)
