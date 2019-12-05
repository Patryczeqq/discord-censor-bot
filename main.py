import discord
import os
import re
from time import localtime

client = discord.Client()

def loadConfig(*configs):
    configs = list(configs)
    output = []
    for config in configs:
        with open("config.txt") as file:
            line = file.readline()
            while line != "":
                if line[:line.index("=")] == config[0]:
                    data = line[line.index("=")+1:-1]
                    if len(data) == 0:
                        data = None
                    elif config[1] == "list":
                        data = data.split(",")
                    elif config[1] == "integer":
                        data = int(data)
                    output.append(data)
                    break
                else:
                    line = file.readline()
            else:
                output.append(None)
    return output

def saveConfig(*configs):
    data = open("config.txt").readlines()
    for config in configs:
        configSaved = False
        for i in range(len(data)):
            seperator = data[i].index("=")
            if data[i][:seperator] == config[0]:
                data[i] = config[0] + "=" + config[1] + "\n"
                configSaved = True
        if not configSaved:
            data.append(config[0] + "=" + config[1] + "\n")
    open("config.txt", "w").write("".join(data))

@client.event
async def on_message(message):
    if message.content.startswith(prefix):
        command = message.content[len(prefix):].split(" ")
        if command[0] == "setprefix":
            prefix = command[1]
            saveConfig(("prefix", prefix))
        else:
            await message.channel.send("Command detected: " + message.content[len(prefix):])
    elif re.match("what (is the )?time (is it)?\??",message.content.lower()):
        time = localtime()
        await message.channel.send(f"The current time is {time[3]}:{time[4]}:{time[5]}")
    elif re.match("what (is the )?(day|date)( is it)?( today)?\??",message.content.lower()):
        time = localtime()
        days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        await message.channel.send(f"Today is {days[time[6]]} {time[2]}/{time[1]}/{time[0]}")
    elif message.channel.name not in exemptChannels:
        text = re.sub("[^a-z]","",message.content.lower())
        if any(bannedWord in text for bannedWord in bannedWords):
            await message.delete()

bannedWords, exemptChannels, prefix = loadConfig(("banned words", "list"), ("exempt channels", "list"), ("prefix", "string"))
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
