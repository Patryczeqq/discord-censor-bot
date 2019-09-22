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
                if line[0] == "#":
                    if line[1:-1] == config:
                        line = file.readline()
                        settings = []
                        while line[0] != "#":
                            settings.append(line[:-1])
                            line = file.readline()
                        output.append(settings)
                        line = ""
                    elif config in line:
                        output.append(line[line.find("=")+1:-1])
                        line = ""
                    else:
                        line = file.readline()
                else:
                    line = file.readline()
    return output

bannedWords, exemptChannels, prefix = loadConfig("banned words", "exempt channels", "prefix")
client = discord.Client()

@client.event
async def on_message(message):
    if message.content.startswith(prefix):
        await message.channel.send("Command detected: " + message.content[len(prefix):])
    elif re.match("is(\s\d+\.?\d*\sinch(es)?\senough\??|.+\stoo\s(short|small)\??)",message.content.lower()):
        await message.channel.send("https://cdn.discordapp.com/attachments/148491526073221120/622438991924297738/unknown.png")
    elif message.channel.name not in exemptChannels:
        text = re.sub("[^a-z]","",message.content.lower())
        if any(bannedWord in text for bannedWord in bannedWords):
            await message.delete()

token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
