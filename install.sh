#!/bin/bash

sudo apt update && sudo apt install -y wget mpv ffmpeg yt-dlp git python3-venv

git clone https://github.com/JohanHelm/cli_youtube.github


### Cкрипт установки и запуска приложения
# Укажите в какую директорию вы хотите установить

cd $HOME/cli_youtube/youtube_api
# Установить венв
touch api_key.py
echo "KEY = ''" >api_key.py

python3 -m venv venv
# Запустить венв
source $HOME/cli_youtube/venv/bin/activate
# Установить pip
# wget https://bootstrap.pypa.io/get-pip.py
# python3 get-pip.py
# rm get-pip.py



pip install -r ./requirements.txt
deactivate
#  Установка самого свежего mpv из деб пакета
# wget https://deb-multimedia.org/pool/main/m/mpv-dmo/mpv_0.36.0-dmo2_amd64.deb
# отсюда https://deb-multimedia.org/dists/testing/main/binary-amd64/package/mpv
# или отсюда https://fruit.je/apt

# create alias for app
echo "alias youtube-cli='$HOME/cli_youtube/venv/bin/python $HOME/cli_youtube/main.py'">> $HOME/.bashrc
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
