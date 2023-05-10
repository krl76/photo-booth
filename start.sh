#!/bin/bash

set -eu

export PYTHONUNBUFFERED=true

VIRTUALENV=./venv
if [ ! -d $VIRTUALENV ]; then
	python3 -m venv $VIRTUALENV
fi

if [ ! -f $VIRTUALENV/bin/pip ]; then
	curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | $VIRTUALENV/bin/python
fi

$VIRTUALENV/bin/pip install -r requirements.txt

$VIRTUALENV/bin/python3 src/main.py &

sleep 5

$VIRTUALENV/bin/python3 src/tgbot.py &

set -e

CHROMIUM_TEMP=~/tmp/chromium

rm -Rf ~/.config/chromium/
rm -Rf $CHROMIUM_TEMP
mkdir -p $CHROMIUM_TEMP

chromium-browser \
    --disable \
    --disable-pinch \
    --private-window \
    --overscroll-history-navigation=0 \
    --dns-prefetch-disable \
    --disable-async-dns \
    --disable-restore-background-contents \
    --incognito \
    --disable-translate \
    --disable-infobars \
    --disable-suggestions-service \
    --disable-save-password-bubble \
    --disk-cache-dir=$CHROMIUM_TEMP/cache/ \
    --user-data-dir=$CHROMIUM_TEMP/user_data/ \
    --start-maximized \
    --kiosk "http://localhost:5000" &
sleep 5
xdotool search --sync --onlyvisible --class "chromium" key F11