# SOCCERNETV2

```bash
conda create -n SoccerNet python pip
pip install SoccerNet
```

## How to Download Games (Python)

```python
from SoccerNet import SoccerNetDownloader

mySoccerNetDownloader = SoccerNetDownloader(
    LocalDirectory="/path/to/soccernet/folder")

# input password to download video (copyright protected)
password = input("Password for videos? (contact the author):\n")
mySoccerNetDownloader.password = password

# Download SoccerNet v1
mySoccerNetDownloader.downloadGames(files=["Labels.json"]) # download labels
mySoccerNetDownloader.downloadGames(files=["1.mkv", "2.mkv"]) # download LQ Videos
mySoccerNetDownloader.downloadGames(files=["1_HQ.mkv", "2_HQ.mkv", "video.ini"]) # download HQ Videos
mySoccerNetDownloader.downloadGames(files=["1_ResNET.npy", "2_ResNET.npy"]) # download Features


# Download SoccerNet Test Set
mySoccerNetDownloader.LocalDirectory = "/path/to/soccernet/test/folder"
mySoccerNetDownloader.downloadTestGames(files=["Labels.json"]) # download labels
mySoccerNetDownloader.downloadTestGames(files=["1.mkv", "2.mkv"]) # download LQ Videos
mySoccerNetDownloader.downloadTestGames(files=["1_HQ.mkv", "2_HQ.mkv", "video.ini"]) # download HQ Videos
mySoccerNetDownloader.downloadTestGames(files=["1_ResNET_TF2.npy", "2_ResNET_TF2.npy"]) # download Features
```

## [Comming...] Tensorflow/Pytorch dataloader

```bash
pip install scikit-video
pip cudnn cudatoolkit=10.1
pip install tensorflow
conda install pytorch torchvision cudatoolkit=10.1 -c pytorch
```
