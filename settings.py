from os import environ as env

# If you don’t know where to get token, follow this tutorial: https://core.telegram.org/bots#3-how-do-i-create-a-bot
# token = <token>
token = env["JOSEE_ACCESS_TOKEN"]

# Checks the current version of the bot with the version on github
check_version = True

# Checks data files and downloads them if they are not found
check_data = False

# Debug levels: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
debug = "INFO"

# Cryptocurrency data update frequency in seconds
crypto_update = 216000

print("Bot Token:\t", token)
