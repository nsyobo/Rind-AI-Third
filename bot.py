import os
import discord
import requests

TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = os.getenv("API_URL")  # https://yourapp.koyeb.app/from-discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot logged in")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    r = requests.post(API_URL, json={
        "text": message.content,
        "channel_id": message.channel.id
    })

    reply = r.json().get("reply")
    await message.channel.send(reply)

client.run(TOKEN)
