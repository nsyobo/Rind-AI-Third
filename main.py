import os
import threading
import discord
import requests
from fastapi import FastAPI
import uvicorn

# ---------- FastAPI ----------
app = FastAPI()

GPTS_ENDPOINT = os.getenv("GPTS_ACTION_ENDPOINT")

@app.post("/to-discord")
def to_discord(data: dict):
    channel_id = os.getenv("DISCORD_CHANNEL_ID")
    message = data.get("message")

    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {os.getenv('DISCORD_TOKEN')}",
        "Content-Type": "application/json"
    }

    requests.post(url, headers=headers, json={
        "content": message
    })

    return {"status": "sent"}
@app.post("/from-discord")
def from_discord(data: dict):
    user_text = data.get("text")

    r = requests.post(
        GPTS_ENDPOINT,
        json={"message": user_text}
    )

    reply = r.json().get("reply", "...")

    return {"reply": reply}


# ---------- Discord Bot ----------
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot online")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    r = requests.post(
        "http://localhost:8000/from-discord",
        json={"text": message.content}
    )

    await message.channel.send(
        r.json().get("reply")
    )

# ---------- Run Both ----------
def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

threading.Thread(target=run_api).start()
client.run(TOKEN)
