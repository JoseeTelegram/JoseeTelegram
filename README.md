# JoseeTelegram

Telegram Bot

## Commands

List of available bot commands, you can also copy and paste them into your bot via [@BotFather](https://t.me/BotFather).

```
8ball - Experiences your future with a magic ball
echo - Repeats your message
coin - Flips a coin
dice - Throws the dice
crypto - Displays the value of the most popular cryptocurrencies
note - Allows to use notes in telegram
cat - Sends a random cat picture
random - Returns a random number from one to argument
remind - Reminds you of your message from the past
repeat - Repeats the message
rgb - Displays RGB to image and HEX
sysfetch - Gets system information
translate - Translates the message into another language
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