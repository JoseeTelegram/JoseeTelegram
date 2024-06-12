# JoseeTelegram

JoseeTelegram is an open-source asynchronous Telegram bot for communication with useful and entertaining commands, aiming for anonymity.

## Description (tl;dr)

Full bot description:
* The bot is JoseeTelegram: the bot is named after a character Josee Yamamura from [Josee, the Tiger and the Fish](https://en.wikipedia.org/wiki/Josee%2C_the_Tiger_and_the_Fish_(2020_film)), don't ask why.
* The bot is open-source: the bot's code is written under the MIT license, which means that you can freely use and edit any part of the code as you wish.
* The bot is asynchronous: the bot is written in [aiogram](https://github.com/aiogram/aiogram), a modern and asynchronous framework Telegram bots in Python.
* The bot is command-driven: the bot works only through commands, using arguments to pass data or using a command as a reply to another message.
* The bot is anonymous: the bot does not store, edit or analyze information about chats, users or messages.

## Commands

List of available bot commands, you can also copy and paste them into your bot via [@BotFather](https://t.me/BotFather).

```
8ball - Experiences your future with a magic ball
echo - Repeats your message
coin - Flips a coin
roll - Makes a dice roll
crypto - Displays the value of the most popular cryptocurrencies
note - Allows to use notes in telegram
cat - Sends a random cat picture
random - Returns a random number from one to argument
remind - Reminds you of your message from the past
repeat - Repeats the message
rgb - Displays RGB to image and HEX
sysfetch - Gets system information
translate - Translates the message into another language
shazam - Recognizes music
```

## Try it

You can try out the functionality using the [official bot deployment](https://t.me/JoseeYamamuraBot) or [deploy it yourself](#deploy).

## Deploy

### Setup

Clone repository:

```bash
$ git clone https://gogs.moonserver.ru/JoseeTelegram/JoseeTelegram
```

Change directory into repository:

```bash
$ cd JoseeTelegram
```

Setup environment variables:

```bash
$ export BOT_TOKEN=<BOT_TOKEN>
```

### Local

Start the bot:

```bash
$ python -m josee_bot
```

### Docker

Create image and start container:

```bash
$ docker-compose up -d
```