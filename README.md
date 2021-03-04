# Guess The ELO Bot

This Discord Bot fetches live 1v1 Random Map Games in an ELO range from aoe2.net.


## Example Usage

1. First, add this bot to your Discord Server.

2. Then, you can use the following commands to find matches within an ELO range. We also create a link to open the game in AoE2: DE (using the same URL that aoe2.net uses).

| Command                         | Description                                                                  | Example Input     |
|:-------------------------------:|:----------------------------------------------------------------------------:|:-----------:|
|`!GetMatchBelow [RATING_CEILING]`| Returns a random match where the combined rating is below `[RATING_CEILING]` | `!GetMatchBelow 2000` |
|`!GetMatchAbove [RATING_FLOOR]`  | Returns a random match where the combined rating is above `[RATING_FLOOR]`   | `!GetMatchAbove 1000` |
|`!GetMatchBetween [LOWER_RATING] [UPPER_RATING]` | Returns a random match between `[RATING_FLOOR]` and `[RATING_CEILING]` | `!GetMatchBetween 1000 2000` |
|`!GetRandomMatch`                | Returns a random match without any ELO constraints. | `!GetRandomMatch` |


## Directory structure

TODO(nanabyte, gnanabit): Outline the directory structure
