import requests
from bs4 import BeautifulSoup
import os

URL = "https://fairystar-ikebukuro.com/cast/6388"
WEBHOOK = os.getenv("WEBHOOK_URL")

def get_schedule():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")

    # ※ここは後で微調整する可能性あり
    schedule = soup.select_one(".schedule")
    return schedule.get_text(strip=True) if schedule else ""

def send_notification(msg):
    if WEBHOOK:
        requests.post(WEBHOOK, json={"content": msg})

def main():
    new_data = get_schedule()

    old_data = ""
    if os.path.exists("last.txt"):
        with open("last.txt", "r") as f:
            old_data = f.read()

    if new_data != old_data:
        added = set(new_data.splitlines()) - set(old_data.splitlines())
        if added:
            send_notification(f"出勤時間が追加されました:\n{added}")

        with open("last.txt", "w") as f:
            f.write(new_data)

if __name__ == "__main__":
    main()
