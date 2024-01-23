# Josee: Telegram Bot

![josee_yamamura](https://wallpapercave.com/wp/wp9333917.jpg)

## Commands

- ``8ball`` - Experiences your future with a magic ball
- ``cat`` - Repeats your message
- ``coin`` - Flips a coin
- ``dice`` - Throws the dice
- ``crypto`` - Displays the value of the most popular cryptocurrencies
- ``note`` - Allows to use notes in telegram
- ``pussy`` - Did you really want to see that?
- ``random`` - Returns a random number from one to argument
- ``remind`` - Reminds you of your message from the past
- ``repeat`` - Repeats the message
- ``rgb`` - Displays RGB to image and HEX
- ``sysfetch`` - Gets system information
- ``translate`` - Translates the message into another language

## Try it

Official bot username: <https://t.me/JoseeYamamuraBot>  
Official bot group: <https://t.me/JoseeYamamuraGroup>  
Be careful, don't click on links similar to these, they can be harmful for you!

# Run The Bot

## Locally

To start the bot, you need to edit *settings.py* and then run *josee.py*.

## Via docker

To create image and start container, edit and run this script:

```
git clone https://github.com/LamberKeep/JoseeTelegram;
cd JoseeTelegram;
docker build --tag 'josee' .;
docker run -e JOSEE_ACCESS_TOKEN=<bot_token> \
 --name josee josee:latest
```