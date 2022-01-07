# Introduction
**A Telegram Bot to force users to join a specific channel before sending messages in a group.**

## Todo
- [ ] Add multiple channels support

## Deploy


[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Installing Prerequisite
- On Ubuntu 18.04 or later
```sh
sudo apt-get install git python3 python3-pip libpq-dev
```

### Installation
- Clone this repo
```sh
git clone https://github.com/viperadnan-git/force-subscribe-telegram-bot
```
- Change directory
```sh
cd force-subscribe-telegram-bot
```
- Install requirements
```sh
pip3 install -r requirements.txt
```

### Configuration
Add [APP_ID](https://my.telegram.org/apps), [API_HASH](https://my.telegram.org/apps), [BOT_TOKEN](https://t.me/botfather) in [Config.py](Config.py) or in Environment Variables.

### Deploying
- Run bot.py
```sh
python3 bot.py
```

## Thanks to
- [PyroGram](https://PyroGram.org)
- [Hasibul Kabir](https://GitHub.com/hasibulkabir) and [Spechide](https://GitHub.com/spechide) for helping.
