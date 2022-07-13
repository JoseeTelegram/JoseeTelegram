import os

import requests
from git import Repo


def check_updates() -> None:
  print("\nSearching for updates...", end=" ")

  try:
    last_commit = requests.get("https://api.github.com/repos/LamberKeep/JoseeTelegram/commits/main").json()['sha']
  except Exception as e:
    print(f"Error: {e}")
    return
  curr_commit = Repo(os.curdir).head.commit.hexsha

  if curr_commit == last_commit:
    print("No new updates avalable.")
  else:
    print("New version avalable, please update!")
