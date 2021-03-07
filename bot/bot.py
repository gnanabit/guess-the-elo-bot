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
async def get_match(ctx):
    # Since ELOs are not uniformly distributed, if we randomly pick a game from
    # the full live matches, then not all ELOs are equally likely to come up.
    # Instead, randomly pick an ELO range and try to find a match from that
    # range.
    #
    # There may be other reasonable ways to try to make the match ELO
    # distribution more fair: e.g., get the live matches, put them into groups
    # based on their ELO range, and pick a uniformly random one of the nonempty
    # ranges, then pick a random game from the chosen range. In this way, all
    # ELO ranges that are represented in live games should be equally likely.
    # However, this method is chosen for simplicity.
    min_elo = random.randint(5, 24) * 100
    max_elo = min_elo + 200
    live_matches = match_fetcher.get_live_matches(min_elo, max_elo)
    if not live_matches:
        # There are no matches in the ELO range -- we will give any live match,
        # if one exists.
        live_matches = match_fetcher.get_live_matches()
    if not live_matches:
        await ctx.send("Couldn't find any matches ... Is AoE2 down?")
    else:
        response = random.choice(live_matches)
        await ctx.send(response)

@get_match_above.error
async def get_match_above_error(ctx, error):
    await ctx.send('Use !help to see the commands I know how to handle.')

@get_match_below.error
async def get_match_below_error(ctx, error):
    await ctx.send('Use !help to see the commands I know how to handle.')

@get_match_between.error
async def get_match_between_error(ctx, error):
    await ctx.send('Use !help to see the commands I know how to handle.')

@get_match.error
async def get_match_error(ctx, error):
    await ctx.send('Use !help to see the commands I know how to handle.')

bot.run(TOKEN)
