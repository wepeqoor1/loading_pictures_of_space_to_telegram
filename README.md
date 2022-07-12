# Images from NASA and SpaceX
Downloading last images and save to directory `images`.
***

## Environment requirements
Python3.10+
***

## How to install
```bash
$ pip install -r requirements.txt
```
***

## Environment variables
Create `.env` file.  
Sign up on https://api.nasa.gov/, get `NASA-API-key` and paste to `.env` file:  
NASA_API_KEY=<`NASA-API-key`>  

Get Telegram API Token:
> Step 1. Find telegram bot named `@botfarther`, he will help you with creating and managing your bot.  
> Step 2. To create a new bot type `/newbot`.
> Step 3. Choose a name for your bot.
> Step 4. Choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.  
> Step 5. Copy `TELEGRAM_API_TOKEN` and paste to `.env` file.

TELEGRAM_API_TOKEN=<`TELEGRAM_API_TOKEN`>
***

# How to use
## For the beginning, download images from SpaceX and NASA API.
### **fetch_nasa_apod_images.py**
>Script taken `required` param `count` (count of images) and download random images of space in directory `images`.
```bash
$ python3 fetch_nasa_apod_images.py <Count of launches>
```

### **fetch_nasa_epic_images.py**
>Script taken `required` param `count` (count of images) and download random images of Earth in directory `images`.
```bash
$ python3 fetch_nasa_epic_images.py <Count of launches>
```

### **fetch_spacex_images.py**
>Script taken `optional` param `--id` (number of ship launch).

If parameter is exists:
>Loads SpaceX images of launch in directory `images`.
```bash
$ python3 fetch_spacex_images.py <launch id>
```

If parameter is `not` exists:
>Loads SpaceX images of last launch in directory `images`.
```bash
$ python3 fetch_spacex_images.py
```
***

## Telegram Bot
### After uploading images of space and launches, start **telegram_bot.py**. 
Script publish in telegram channel message and upload image of space from directory (default `images/` from `config.py`) every (default 4 hours from `config.py`) 
```bash
$ python3 telegram_bot.py
```
