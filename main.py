import discord
import os
import re

bannedWords = ["bruh"]
exemptChats = ["bruh-chat"]
client = discord.Client()

@client.event
async def on_message(message):
    if message.channel.name != "bruh":
        text = re.sub("[^a-z]","",message.content.lower())
        if any(bannedWord in text for bannedWord in bannedWords):
            await message.delete()

token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)