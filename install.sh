#!/usr/bin/env bash
sudo apt-get install nginx uwsgi uwsgi-plugin-python3 python3-pip memcached python3-dev libffi-dev
sudo pip3 install -r ./python_package_list
chmod +x manage.py
chmod +x start.sh
mkdir document
cp ./config/menu.example.json ./config/menu.json
cp ./config/page.example.json ./config/page.json
cp ./config/system.example.json ./config/system.json
vim ./config/system.json