import requests
import os

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

requests.post(WEBHOOK_URL, json={
    "content": "テスト通知です"
})
