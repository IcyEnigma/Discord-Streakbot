import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix='+')


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.command()
async def init(ctx):
    botUser = ctx.author
    datajson = open(r"./data.json", 'r')
    jsonFile = json.loads(datajson.read())
    [userVal, userCheck] = fetchUser(ctx.author, jsonFile['elements'])
    userCheck = False
    for element in jsonFile['elements']:
        if user.id == element['user_id']:
            userCheck = True
    if userCheck:
        await ctx.send(f"{ctx.author.mention} has already been initialized.")
    else:
        jsonFile['elements'].append({
            'name': botUser.name,
            'mention': botUser.mention,
            'user_id': botUser.id,
        })
        datajson.close()
        datajsonOut = open(r"./data.json", 'w')
        datajsonOut.write(json.dumps(jsonFile))
        datajsonOut.close()
        await ctx.send(f"{ctx.author.mention} has been initialized as a User.")

    print("New user initialized ", jsonFile['elements'])





client.run(TOKEN)
