"""Fetches 1v1 Random Map in an ELO range from aoe2.net

Typical usage example:
# TODO: add usage examples.
"""

import argparse
import match_fetcher


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get live matches in ' \
                                     'specified range')
    parser.add_argument('--min-avg-rating', type=int, default=0,
                        help='the minimum average rating of the ELO range. ' \
                        'Default value is 0')
    parser.add_argument('--max-avg-rating', type=int, default=3000,
                        help='the maximum average rating of the ELO range. ' \
                        'Default value is 3000')
    parser.add_argument('--count', type=int, default=100,
                        help='the number of games to get from aoe2.net, ' \
                        'which will likely not be the number of games shown. ' \
                        'Default value is 100')
    parser.add_argument('--max-time-since-start', type=int, default=10,
                        help='the maximum time since the game has started, ' \
                        'in minutes. Decrease to make it more likely to see ' \
                        'a longer list of games. Default value is 10')
    args = parser.parse_args()
    print(match_fetcher.get_live_matches(args.min_avg_rating,
                                         args.max_avg_rating, args.count,
                                         args.max_time_since_start))
