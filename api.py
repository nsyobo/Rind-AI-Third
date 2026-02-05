from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

GPTS_ACTION_ENDPOINT = os.getenv("GPTS_ACTION_ENDPOINT")

class DiscordIn(BaseModel):
    text: str
    channel_id: str

@app.post("/from-discord")
def from_discord(data: DiscordIn):

    # GPTs Actionに送る
    r = requests.post(
        GPTS_ACTION_ENDPOINT,
        json={"message": data.text}
    )

    gpt_reply = r.json().get("reply", "……")

    return {"reply": gpt_reply}


# GPTs → Discord 用
@app.post("/to-discord")
def to_discord(data: dict):
    return {"status": "ok"}
