#!/bin/bash

# install neccesary utilites
sudo apt update && sudo apt install -y wget mpv ffmpeg yt-dlp git python3-venv
# clone the app
git clone https://github.com/JohanHelm/cli_youtube.git $(HOME)/.local/share/cli_youtube

cd $(HOME)/.local/share/cli_youtube
# create file for api key
touch youtube_api/api_key.py
echo "KEY = ''" > youtube_api/api_key.py

# create venv
python3 -m venv venv
# activate venv
source $(HOME)/.local/share/cli_youtube/venv/bin/activate

# instal requirements
pip install -r ./requirements.txt
deactivate


# create alias for app
echo "alias youtube-cli='$(HOME)/.local/share/cli_youtube/venv/bin/python $(HOME)/.local/share/cli_youtube/main.py'">> $HOME/.bashrc
source $HOME/.bashrc


# paste scripts into ~/.config/mpv/scripts
cd $HOME/.config/mpv/scripts
# resolution
# https://github.com/jgreco/mpv-youtube-quality
wget https://github.com/jgreco/mpv-youtube-quality/raw/master/youtube-quality.lua

# sponsoreblock
# https://github.com/po5/mpv_sponsorblock
wget https://github.com/po5/mpv_sponsorblock/raw/master/sponsorblock.lua
mkdir sponsorblock_shared
cd sponsorblock_shared
wget https://github.com/po5/mpv_sponsorblock/raw/master/sponsorblock_shared/main.lua
wget https://github.com/po5/mpv_sponsorblock/raw/master/sponsorblock_shared/sponsorblock.py
