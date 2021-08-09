import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
print("Hello")
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
         await message.reply('Hello!', mention_author=True)

client.run(TOKEN)
