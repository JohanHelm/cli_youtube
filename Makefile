# common goal
setup: update install_utils clone install_pip create_venv install_req create_alias usefull_scripts

update:  # Update packages
	apt update
	
install_utils:  # install neccesary utilites
	apt install -y wget mpv ffmpeg yt-dlp git
	
clone:  # clone the app from github
	git clone https://github.com/JohanHelm/cli_youtube.git	
	
install_pip:  #install pip 
	cd $HOME/cli_youtube
	apt install -y python3-venv

create_venv:  #create and activate venv
	python3 -m venv venv
	source $HOME/cli_youtube/venv/bin/activate
	
install_req:  #install requirements
	pip install -r ./requirements.txt
	deactivate
	
create_alias:  #create alias for application
	echo "alias youtube-cli='$HOME/cli_youtube/venv/bin/python $HOME/cli_youtube/main.py'">> $HOME/.bashrc
	source $HOME/.bashrc
	
usefull_scripts:  # paste scripts into ~/.config/mpv/scripts
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
	
.PHONY: update install_utils clone install_pip create_venv install_req create_alias usefull_scripts

