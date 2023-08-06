
from pathlib import Path
import json
import os


def getListGames(jsonGamesFile=None):

    if jsonGamesFile is None:
        jsonGamesFile = Path(__file__).parent / "data/SoccerNetGames.json"

    print("jsonGamesFile:", jsonGamesFile)
    # print(Path(__file__).parent+"data/cap_data.txt")
    with open(jsonGamesFile, "r") as json_file:
        dictionary = json.load(json_file)

    for championship in dictionary:
        for season in dictionary[championship]:
            for game in dictionary[championship][season]:

                game = os.path.join(championship, season, game)
                yield(game)


def getListTestGames(jsonGamesFile=None):

    if jsonGamesFile is None:
        jsonGamesFile = Path(__file__).parent / "data/SoccerNetTestGames.json"

    print("jsonGamesFile:", jsonGamesFile)
    # print(Path(__file__).parent+"data/cap_data.txt")
    with open(jsonGamesFile, "r") as json_file:
        dictionary = json.load(json_file)

    for championship in dictionary:
        for season in dictionary[championship]:
            for game in dictionary[championship][season]:

                game = os.path.join(championship, season, game)
                yield(game)


if __name__ == "__main__":
    print(len([r for r in getListTestGames()]))
