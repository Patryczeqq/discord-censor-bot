import discord
import os
import re

def loadConfig(*configs):
    configs = list(configs)
    output = []
    for config in configs:
        with open("config.txt") as file:
            line = file.readline()
            while line != "":
                if line[0] == "#" and line[1:-1] == config:
                    line = file.readline()
                    settings = []
                    while line[0] != "#":
                        settings.append(line[:-1])
                        line = file.readline()
                    output.append(settings)
                    line = ""
                else:
                    line = file.readline()
    return output

bannedWords, exemptChannels = loadConfig("banned words", "exempt channels")
client = discord.Client()

@client.event
async def on_message(message):
    print(message.channel.name)
    if message.channel.name not in exemptChannels:
        text = re.sub("[^a-z]","",message.content.lower())
        if any(bannedWord in text for bannedWord in bannedWords):
            await message.delete()
    if re.match("is(\s\d+\.?\d*\sinch(es)?\senough\??|.+\stoo\s(short|small)\??)",message.content.lower()):
        await message.channel.send("https://cdn.discordapp.com/attachments/148491526073221120/622438991924297738/unknown.png")

token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
