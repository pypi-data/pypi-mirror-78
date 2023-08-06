# SOCCERNETV2

conda create -n SoccerNet python pip
pip install SoccerNet

## How to Download Games (Python)

from SoccerNet import SoccerNetDownloader

mySoccerNetDownloader = SoccerNetDownloader(
    LocalDirectory="/path/to/soccernet/folder")

password = input("Password for videos? (contact the author):\n")

mySoccerNetDownloader.password = password

mySoccerNetDownloader.downloadTestGames(files=["Labels.json"]) # download labels
mySoccerNetDownloader.downloadTestGames(files=["1.mkv", "2.mkv"]) # download LQ Videos
mySoccerNetDownloader.downloadTestGames(files=["1_HQ.mkv", "2_HQ.mkv"]) # download HQ Videos

## [Dev] Tensorflow/Pytorch dataloader

pip install scikit-video
pip cudnn cudatoolkit=10.1
pip install tensorflow
conda install pytorch torchvision cudatoolkit=10.1 -c pytorch
