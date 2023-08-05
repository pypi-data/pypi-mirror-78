
import urllib.request
import os
from tqdm import tqdm
# import progressbar
import json
from libs.downloader import OwnCloudDownloader, SoccerNetDownloader

if __name__ == "__main__":
    # from libs.downloader import SoccerNetDownloader

    mySoccerNetDownloader = SoccerNetDownloader(
        LocalDirectory="/media/giancos/Football/SoccerNet_HQ",
        include_Video=True)

    mySoccerNetDownloader.downloadGames(jsonGamesFile="src/SoccerNet.json")
