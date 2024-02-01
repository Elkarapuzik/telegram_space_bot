# Telegram star bot
- This is a program that automatically sends pictures and messages to Telegram using the SpaceX and NASA database.
## How to install
- Download the repository from the git hub:

```
https://github.com/Elkarapuzik/telegram_space_bot
```

- Python3 should already be installed. Then use pip(or pip3 if there is a conflict with Python2) to install dependencies:

```
pip install -r requirements.txt
``` 
## Preparing to run
- Go to the NASA API site, register, get your token
- Register your Telegram bot and get its API token.
- Create a `.env` file in the program folder.
- The `.env` file should have the following form:
```
API_KEY=*NASA token*
TELEGRAM_BOT_TOKEN=*API telegram token*
TELEGRAM_CHAT_ID=*Link to telegram bot with @ instead of t.me/*(example : @tailer_derden_kanal)
```

## How to run the program
- To run the program you need to type in the command line:
```
python3 main.py
```