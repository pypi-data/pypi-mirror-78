
from libs.downloader import SoccerNetDownloader

mySoccerNetDownloader = SoccerNetDownloader(
    LocalDirectory="/media/giancos/Football/SoccerNet_HQ",
    include_Video=True)

mySoccerNetDownloader.downloadGames(jsonGamesFile="games.json")
