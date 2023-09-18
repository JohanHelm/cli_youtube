#!/bin/bash

apt update
apt install wget mpv ffmpeg yt-dlp git
### Cкрипт установки и запуска приложения
# Укажите в какую директорию вы хотите установить
your_dir=~/youtube-cli
# Создать каталог
mkdir $your_dir
cd $your_dir
# Установить венв
python3 -m venv $your_dir
# Запустить венв
source $your_dir/bin/activate
# Установить pip
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
rm get-pip.py

git clone  
pip install -R requirements.txt
#  Установка самого свежего mpv из деб пакета
# wget https://deb-multimedia.org/pool/main/m/mpv-dmo/mpv_0.36.0-dmo2_amd64.deb
# отсюда https://deb-multimedia.org/dists/testing/main/binary-amd64/package/mpv
# или отсюда https://fruit.je/apt

