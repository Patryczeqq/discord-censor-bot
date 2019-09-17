import discord
import os
import re

bannedWords = ["fortnite", "smeltery"]
exemptChannels = ["bruh-chat"]
client = discord.Client()

@client.event
async def on_message(message):
    print(message.channel.name)
    if message.channel.name not in exemptChannels:
        text = re.sub("[^a-z]","",message.content.lower())
        if any(bannedWord in text for bannedWord in bannedWords):
            await message.delete()
    if message.content.lower() == "is 4.2 inches enough?":
        message.channel.send("https://cdn.discordapp.com/attachments/148491526073221120/622438991924297738/unknown.png")

token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
