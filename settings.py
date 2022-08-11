import os

# If you don’t know where to get token, follow this tutorial: https://core.telegram.org/bots#3-how-do-i-create-a-bot
token = os.environ["JOSEE_ACCESS_TOKEN"] # heroku
# token = "ACCESS_TOKEN" # local

# Your ID is required to receive error messages directly in PM.
# It can be obtained by writing the "/start" to the bot: https://t.me/userinfobot.
# Leave the value at 0 to disable this feature. (But why?)
id = os.environ["JOSEE_MY_ID"] # heroku
# id = 0 # local

# Checks the current version of the bot with the version on github.
check_version = False

# Checks data files and downloads them if they are not found.
check_data = False

# Debug levels: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL".
debug = "WARNING"