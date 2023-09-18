#!/bin/bash

apt update
apt install -y wget mpv ffmpeg yt-dlp git
### Cкрипт установки и запуска приложения
# Укажите в какую директорию вы хотите установить
your_dir=~/youtube-cli
# Создать каталог
mkdir $your_dir
cd $your_dir
# Установить венв
apt install -y python3-venv
python3 -m venv venv
# Запустить венв
source $your_dir/venv/bin/activate
# Установить pip
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
rm get-pip.py

git clone https://github.com/JohanHelm/cli_youtube.git

pip install -r ./requirements.txt
#  Установка самого свежего mpv из деб пакета
# wget https://deb-multimedia.org/pool/main/m/mpv-dmo/mpv_0.36.0-dmo2_amd64.deb
# отсюда https://deb-multimedia.org/dists/testing/main/binary-amd64/package/mpv
# или отсюда https://fruit.je/apt

# create alias for app
echo "alias youtube='~/youtube-cli/venv/bin/python main.py'">> ~/.bashrc
source ~/.bashrc


# paste scripts into ~/.config/mpv/scripts
# sponsoreblock
# https://github.com/po5/mpv_sponsorblock
wget https://github.com/po5/mpv_sponsorblock/raw/master/sponsorblock.lua
mkdir sponsorblock_shared
cd sponsorblock_shared
wget https://github.com/po5/mpv_sponsorblock/raw/master/sponsorblock_shared/main.lua
wget https://github.com/po5/mpv_sponsorblock/raw/master/sponsorblock_shared/sponsorblock.py

# resolution
# https://github.com/jgreco/mpv-youtube-quality
wget https://github.com/jgreco/mpv-youtube-quality/raw/master/youtube-quality.lua

    
