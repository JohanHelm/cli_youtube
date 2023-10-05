.PHONY: install venv alias mpv-scripts

install: apt-install venv alias mpv-scripts

apt-install:
    @sudo apt update
    @sudo apt install -y wget mpv ffmpeg yt-dlp git python3-venv

venv:
    @git clone https://github.com/JohanHelm/cli_youtube.git $(HOME)/cli_youtube
    @cd $(HOME)/cli_youtube/youtube_api && touch api_key.py && echo "KEY = ''" > api_key.py
    @python3 -m venv $(HOME)/cli_youtube/venv
    @. $(HOME)/cli_youtube/venv/bin/activate && pip install -r $(HOME)/cli_youtube/requirements.txt && deactivate

alias:
    @echo "alias youtube-cli='$(HOME)/cli_youtube/venv/bin/python $(HOME)/cli_youtube/main.py'" >> $(HOME)/.bashrc
    @. $(HOME)/.bashrc

mpv-scripts:
    @mkdir -p $(HOME)/.config/mpv/scripts/sponsorblock_shared
    @cd $(HOME)/.config/mpv/scripts && wget https://github.com/jgreco/mpv-youtube-quality/raw/master/youtube-quality.lua
    @cd $(HOME)/.config/mpv/scripts && wget https://github.com/po5/mpv_sponsorblock/raw/master/sponsorblock.lua
    @cd $(HOME)/.config/mpv/scripts/sponsorblock_shared && wget https://github.com/po5/mpv_sponsorblock/raw/master/sponsorblock_shared/main.lua
    @cd $(HOME)/.config/mpv/scripts/sponsorblock_shared && wget https://github.com/po5/mpv_sponsorblock/raw/master/sponsorblock_shared/sponsorblock.py
