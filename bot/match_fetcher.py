"""Library for fetching live 1v1 Random Map games in an ELO range from aoe2.net

Typical usage example:
# TODO: add usage examples.
"""
import json
import time
from urllib import request

# Get the id to human-readable information mapping.  Maps in the match data are
# described by their IDs (e.g., id = 9 for Arabia). This allows us to translate
# the match data into a human-understandable format.
strings_url = 'https://aoe2.net/api/strings?game=aoe2de&language=en'
id_info = json.loads(request.urlopen(strings_url).read().decode())

def get_live_matches(min_avg_rating=0, max_avg_rating=3000, count=100,
                     max_time_since_start=10):
    """Prints several in-progress AUTOMATCHes in the specified ELO range.

    The ELO range is specified by a maximum and minimum for the average ELO of
    the two players.

    Args:
        min_avg_rating: the minimum average rating of the ELO range.
        max_avg_rating: the maximum average rating of the ELO range.
        count: the number of matches to get from aoe2.net. This number should be
          large in order to increase the number of results provided, although a
          count of 100 doesn't guarantee that 100 matches will be listed.
        max_time_since_start: the maximum age of the game, in minutes. Giving a
          lower number will probably increase the number of games shown, since
          the games from aoe2.net will have started more recently and will
          likely be unfinished.
    """
    start_epochtime = int(time.time()) - 60 * max_time_since_start
    curr_games_url = 'https://aoe2.net/api/matches?game=aoe2de' \
        '&count={!s}&since={!s}'.format(count, start_epochtime)
    games = json.loads(request.urlopen(curr_games_url).read().decode())
    valid_games = []
    for game in games:
        if match_in_range(game, min_avg_rating, max_avg_rating):
            valid_games.append(match_info_string(game))
    return valid_games

def match_in_range(game, min_avg_rating, max_avg_rating):
    """Checks whether the game is in the specified elo range.

    Args:
        game: the game information in the format obtained from aoe2.net
        min_avg_rating: the minimum average rating of the ELO range.
        max_avg_rating: the maximum average rating of the ELO range.

    Returns:
        True if the game is a 1v1 AUTOMATCH that is in progress,
    """
    # Some games have 'average_rating' as None, even if both players are
    # rated. Until I figure out why, I will check that the average rating isn't
    # None. The 'leaderboard_id' can also be None.
    return (not game['leaderboard_id'] == None
            and (id_info['leaderboard'][game['leaderboard_id']]['string']
                 == '1v1 Random Map')
            and game['finished'] == None
            and not game['average_rating'] == None
            and min_avg_rating <= game['average_rating']
            and game['average_rating'] <= max_avg_rating)

def match_info_string(game):
    """Returns human-readable information about the match.

    A sample format:
    12345678: Genghis Khan (Mongols) vs. Khwarazm (Persians) on Arabia

    Parameters:
    -----------
    game : dict
           the game information in the format obtained from aoe2.net
    """
    player0 = game['players'][0]
    player1 = game['players'][1]
    map_name = None
    # id_info['civ'] and id_info['map_type'] are lists of maps so we need
    # to find the map type (currently the id starts at 9 for Arabia, but it's
    # not clear if this will change). The civ list is more clearly done (id
    # starts at 0 and goes up to 36), so we can get the element at the civ id
    # and get its string.
    for map_entry in id_info['map_type']:
        if map_entry['id'] == game['map_type']:
            map_name = map_entry['string']
            break
    return "{!s}: {!s} ({!s}) vs. {!s} ({!s}) on {!s}. Open game: https://aoe2.net/s/{!s}"\
        .format(game['match_id'],
                player0['name'], id_info['civ'][player0['civ']]['string'],
                player1['name'], id_info['civ'][player1['civ']]['string'],
                map_name, game['match_id'])
