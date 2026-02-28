import requests
from bs4 import BeautifulSoup
import datetime
import hashlib
import os

DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
TARGET_URL = "https://www.31sumai.com/attend/X2571/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/111.0.0.0 Safari/537.36"
    )
}

def send_discord_message(message: str):
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

def get_page_hash(url: str):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    text = " ".join(soup.get_text().split())
    return hashlib.md5(text.encode("utf-8")).hexdigest()

HASH_FILE = "previous_hash.txt"

try:
    current_hash = get_page_hash(TARGET_URL)

    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            previous_hash = f.read().strip()
    else:
        previous_hash = None

    if previous_hash and current_hash != previous_hash:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_discord_message(
            f"🔔 ページに変化がありました！\nURL: {TARGET_URL}\n通知時刻: {now}"
        )

    with open(HASH_FILE, "w") as f:
        f.write(current_hash)

except Exception as e:
    print(f"Error: {e}")
