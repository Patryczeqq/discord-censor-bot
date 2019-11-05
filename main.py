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
                if line[:line.index("=")] == config:
                    data = line[line.index("=")].split(",")
                    if len(data) == 1:
                        data = data[0]
                    elif len(data) == 0:
                        data = None
                    output.append(data)
                    break
                else:
                    line = file.readline()
            else:
                output.append(None)
    return output

bannedWords, exemptChannels, prefix = loadConfig("banned words", "exempt channels", "prefix")
client = discord.Client()

@client.event
async def on_message(message):
    if message.content.startswith(prefix):
        await message.channel.send("Command detected: " + message.content[len(prefix):])
    elif re.match("is.+(too\s(short|small)|enough)\??)",message.content.lower()):
        await message.channel.send("https://cdn.discordapp.com/attachments/148491526073221120/622438991924297738/unknown.png")
    elif message.channel.name not in exemptChannels:
        text = re.sub("[^a-z]","",message.content.lower())
        if any(bannedWord in text for bannedWord in bannedWords):
            await message.delete()

token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
