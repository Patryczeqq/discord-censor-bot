import discord
import os
import re
import requests
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
    if len(output) == 1:
        return output[0]
    return output

def saveConfig(*configs):
    data = open("config.txt").readlines()
    configs = list(configs)
    for config in configs:
        config = list(config)
        if type(config[1]) == list:
            config[1] = ",".join(config[1])
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
async def on_member_remove(member):
    if member.guild.system_channel:
        await member.guild.system_channel.send(member.nick + " has left the server")

@client.event
async def on_message(message):
    bannedWords, exemptChannels, prefix = loadConfig(("banned words", "list"), ("exempt channels", "list"), ("prefix", "string"))
    if message.content.startswith(prefix):
        command = message.content[len(prefix):].split(" ")
        if command[0] == "setprefix":
            prefix = command[1]
            saveConfig(("prefix", prefix))
            await message.channel.send("Successfuly changed prefix to " + prefix)
        elif command[0] == "banword":
            wordToBan = command[1].lower()
            if wordToBan not in bannedWords:
                bannedWords.append(wordToBan)
                saveConfig(("banned words", bannedWords))
                await message.channel.send("Successfuly banned word " + wordToBan)
            else:
                await message.channel.send("Error: " + command[1] + " is already banned")
        elif command[0] == "unbanword":
            wordToUnban = command[1].lower()
            if wordToUnban in bannedWords:
                bannedWords.remove(wordToUnban)
                saveConfig(("banned words", bannedWords))
                await message.channel.send("Successfuly unbanned word " + wordToUnban)
            else:
                await message.channel.send("Error: " + command[1] + " is not banned")
        elif command[0] == "bannedwords":
            await message.channel.send("Banned words are:\n`" + "`\n`".join(bannedWords) + "`")
        elif command[0] == "dbd":
            if len(command) == 1:
                await message.channel.send(
'''DBD COMMAND LIST
`randsurv`/`randkill`: Generates a random build
`perktypes`: lists all valid perk types
`perktype <type>`: lists all perks of that type
`shrine`: shows what is in the current shrine
`playercount`: number of players currently in-game
''')
            elif command[1].startswith("rand"):
                reqType = {"surv":"survivor", "kill":"killer"}[command[1][-4:]] 
                await message.channel.send(requests.get(f"https://dbd.onteh.net.au/api/randomperks?role={reqType}&pretty").text)
            elif command[1] == "perktypes":
                perks = requests.get("https://dbd.onteh.net.au/api/perks").json()
                categories = set()
                for perkID in perks:
                    print(perks[perkID])
                    categories.update(perks[perkID]["categories"])
                await message.channel.send(", ".join(categories))
            elif command[1] == "perktype":
                perks = requests.get("https://dbd.onteh.net.au/api/perks").json()
                await message.channel.send(", ".join([perks[perkID]["name"] for perkID in perks if command[2] in perks[perkID]["categories"]]))
            elif command[1] == "playercount":
                await message.channel.send(requests.get("https://dbd.onteh.net.au/api/playercount?pretty").text)
            elif command[1] == "shrine":
                await message.channel.send(requests.get("https://dbd.onteh.net.au/api/shrine?pretty").text)
        else:
            await message.channel.send("Command detected: " + command[0])
    elif re.match("what (is the )?time( is it)?\??",message.content.lower()):
        time = localtime()
        await message.channel.send(f"The current time is {time[3]}:{time[4]}:{time[5]}")
    elif re.match("what (is the )?(day|date)( is it)?( today)?\??",message.content.lower()):
        time = localtime()
        days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        await message.channel.send(f"Today is {days[time[6]]} {time[2]}/{time[1]}/{time[0]}")
    elif message.channel.name not in exemptChannels and message.author.bot == False:
        text = re.sub("[^a-z]","",message.content.lower())
        if any(bannedWord in text for bannedWord in bannedWords):
            await message.delete()

token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
