### Cкрипт установки и запуска бота на ВПС в виртуальном окружении
# Укажите в какую директорию вы хотите установить
your_dir=/home/pp/Mu_bot
# Создать каталог
mkdir $your_dir
# Установить венв
python3 -m venv $your_dir
# Запустить венв
source $your_dir/bin/activate
# Установить pip
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
