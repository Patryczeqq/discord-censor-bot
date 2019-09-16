import discord
import os
import re

print("Setting up...")

bannedWords = ["bruh"]
exemptChats = ["bruh-chat"]
client = discord.Client()

@client.event
async def on_message(message):
    if message.channel.name != "bruh":
        text = re.sub("[^a-z]","",message.content.lower())
        if any(bannedWord in text for bannedWord in bannedWords):
            await message.delete()

print("Setup complete")

token = os.environ.get("DISCORD_BOT_SECRET")
print("test")
client.run(token)
print("done")
