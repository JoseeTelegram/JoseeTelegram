import os

import requests


def check_files() -> None:
    print("\nChecking data files...")

    if not os.path.exists("data"):
        os.mkdir("data")

    files_data = ["8ball.txt", "crypto.json", "notes.json", "cat.jpg"]
    for i in files_data:
        print(f"{i}...", end=" ")
        if not os.path.exists(f"data/{i}"):
            print("fail, downloading the file")
            file = open(f"data/{i}", "w")
            file.write(
                requests.get(f"https://raw.githubusercontent.com/Josee-Yamamura/JoseeTelegram/main/data/{i}").text)
            file.close()
        else:
            print("ok")

    if not os.path.exists("cache"):
        os.mkdir("cache")
