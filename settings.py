from os import environ as env

# If you don’t know where to get token, follow this tutorial: https://core.telegram.org/bots#3-how-do-i-create-a-bot
token = env["JOSEE_ACCESS_TOKEN"]

# Your ID is required to receive error messages directly in PM.
# It can be obtained by writing the "/start" to the bot: https://t.me/userinfobot.
id = env["JOSEE_MY_ID"].split(",")

# Checks the current version of the bot with the version on github.
check_version = True

# Checks data files and downloads them if they are not found.
check_data = False

# Debug levels: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL".
debug = "INFO"