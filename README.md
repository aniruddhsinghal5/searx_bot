# Searx Bot

[Telegram bot](https://t.me/ssearx_bot) to search in any Searx instance in your group or direct message.

## Usage

Use `/start` or `/help` option to display available commands.

## Self-hosting

+ Clone this repo.
```
$ git clone https://git.samedamci.me/samedamci/searx_bot && cd searx_bot
```
+ Install required modules.
```
$ pip3 install --user -r requirements.txt
```
+ Create `environment` file with your bot token and instance URL.
```
TOKEN=your_token_here
INSTANCE_URL=https://searx.example.com
```
+ Start bot with `python3 main.py`.

### With Docker

+ Download Docker image from [GitHub Packages](https://github.com/samedamci/searx_bot/packages).

+ Alternatively build image itself.
```
# docker build -t samedamci/searx_bot .
```
+ Run bot in container.
```
# docker run --rm -d -e TOKEN='your_token_here' \
	-e INSTANCE_URL='https://searx.example.com' \
	--name searx_bot samedamci/searx_bot
```
