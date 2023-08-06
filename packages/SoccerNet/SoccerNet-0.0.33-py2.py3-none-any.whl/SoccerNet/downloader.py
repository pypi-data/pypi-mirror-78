
from pathlib import Path
import urllib.request
import os
from tqdm import tqdm
# import progressbar
import json

class MyProgressBar():
    def __init__(self, filename):
        self.pbar = None
        self.filename = filename

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar = tqdm(total=total_size, unit='iB', unit_scale=True)
            self.pbar.set_description(f"Downloading {self.filename}...")
            self.pbar.refresh()  # to show immediately the update

        self.pbar.update(block_size)



class OwnCloudDownloader():
    def __init__(self, LocalDirectory, OwnCloudServer):
        self.LocalDirectory = LocalDirectory
        self.OwnCloudServer = OwnCloudServer

    def downloadFile(self, path_local, path_owncloud, user=None, password=None):
        # return 0: successfully downloaded
        # return 1: HTTPError
        # return 2: unsupported error

        try:
            try:
                password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
                password_mgr.add_password(
                    None, self.OwnCloudServer, user, password)
                handler = urllib.request.HTTPBasicAuthHandler(
                    password_mgr)
                opener = urllib.request.build_opener(handler)
                urllib.request.install_opener(opener)

                urllib.request.urlretrieve(
                    path_owncloud, path_local, MyProgressBar(path_local))

            except urllib.error.HTTPError as identifier:
                print(identifier)
                return 1

        except:
            os.remove(path_local)
            raise
            return 2
        return 0


class SoccerNetDownloader(OwnCloudDownloader):
    def __init__(self, LocalDirectory, 
    OwnCloudServer="https://exrcsdrive.kaust.edu.sa/exrcsdrive/public.php/webdav/", 
    include_Video=False):
        super(SoccerNetDownloader, self).__init__(
            LocalDirectory, OwnCloudServer)
        self.include_Video = include_Video
        self.password = None


    def downloadGame(self, game):

        GameDirectory = os.path.join(self.LocalDirectory, game)
        GameURL = os.path.join(self.OwnCloudServer, game).replace(' ', '%20')
        os.makedirs(GameDirectory, exist_ok=True)

        # if include vide
        if self.include_Video:
            if self.password is None:
                self.password = input("Key for videos?:\n") 
            
            for file in ["video.ini", "1_HQ.mkv", "2_HQ.mkv"]:

                GameFile = os.path.join(GameDirectory, file)
                OwnCloudFile = os.path.join(GameURL, file).replace(' ', '%20')

                if os.path.exists(GameFile):
                    print(f"{GameFile} already exists")
                    continue

                # while not res == 0:
                res = self.downloadFile(path_local=GameFile,
                                        path_owncloud=OwnCloudFile,
                                        user="B72R7dTu1tZtIst",  # URL for video HQ
                                        password=self.password)





    def downloadGames(self, jsonGamesFile=None):

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
                    self.downloadGame(game)

    def downloadTestGames(self, jsonGamesFile=None, files=["1.mkv", "2.mkv", "Labels.json"]):

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
                    # self.downloadGame(game)

                    GameDirectory = os.path.join(self.LocalDirectory, game)
                    GameURL = os.path.join(self.OwnCloudServer, game).replace(' ', '%20')
                    os.makedirs(GameDirectory, exist_ok=True)


                    for file in ["1.mkv","2.mkv"]:
                        if file not in files:
                            continue
                        GameFile = os.path.join(GameDirectory, file)
                        OwnCloudFile = os.path.join(GameURL, file).replace(' ', '%20')

                        if os.path.exists(GameFile):
                            print(f"{GameFile} already exists")
                            continue

                        # while not res == 0:
                        res = self.downloadFile(path_local=GameFile,
                                                path_owncloud=OwnCloudFile,
                                                user="trXNXsW9W04onBh",  # URL for video HQ
                                                password=self.password)

                    for file in ["1_HQ.mkv", "2_HQ.mkv", "video.ini"]:
                        if file not in files:
                            continue
                        GameFile = os.path.join(GameDirectory, file)
                        OwnCloudFile = os.path.join(
                            GameURL, file).replace(' ', '%20')

                        if os.path.exists(GameFile):
                            print(f"{GameFile} already exists")
                            continue

                        # while not res == 0:
                        res = self.downloadFile(path_local=GameFile,
                                                path_owncloud=OwnCloudFile,
                                                user="eLc2pGDuTHeDztj",  # URL for video HQ
                                                password=self.password)

                    for file in ["Labels.json"]:
                        if file not in files:
                            continue
                        GameFile = os.path.join(GameDirectory, file)
                        OwnCloudFile = os.path.join(
                            GameURL, file).replace(' ', '%20')

                        if os.path.exists(GameFile):
                            print(f"{GameFile} already exists")
                            continue

                        # while not res == 0:
                        res = self.downloadFile(path_local=GameFile,
                                                path_owncloud=OwnCloudFile,
                                                user="WUOSnPSYRC1RY13",  # URL for video HQ
                                                password=self.password)


                    

# REQUESTS
# from tqdm import tqdm
# import requests

# SoccerNetDir = "/media/giancos/Football/SoccerNet_HQ"
# toplevel_url = "https://exrcsdrive.kaust.edu.sa/exrcsdrive/public.php/webdav/"
# game = "england_epl/2014-2015/2015-02-21 - 18-00 Crystal Palace 1 - 2 Arsenal"
# file = "video.ini"


# import os
# for file in ["video.ini", "1_HQ.mkv", "2_HQ.mkv"]:

#     user, password = 'B72R7dTu1tZtIst', 'SoccerNet'
#     response = requests.get(f"{toplevel_url}/{game.replace(' ','%20')}/{file}", auth=(user, password), stream=True)
#     total_size_in_bytes= int(response.headers.get('content-length', 0))

#     filename = f"{game}/{file}"

#     if os.path.exists(filename):
#         print(f"{filename} already downloaded")
#         continue
#     try:
#         progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
#         progress_bar.set_description(f"Downloading {filename}...")
#         progress_bar.refresh() # to show immediately the update
#         with open(filename, "wb") as handle:
#             for data in response.iter_content():
#                 progress_bar.update(len(data))
#                 handle.write(data)
#     except:
#         os.remove(filename)
#         raise
#     print("Download complete for %s!" % filename)
