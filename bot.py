import discord
from discord.ext import commands
import os
import json
from datetime import date
import asyncio
import sqlFunctions as sf

client = commands.Bot(command_prefix='*')


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command()
async def hi(ctx):
    await ctx.send(f"Hi there {ctx.author.name}!")

@client.command()
async def init(ctx):
    botUser = ctx.author
    userList = sf.getUsers()
    userCheck = False
    for user in userList:
        if str(botUser.id) == user:
            userCheck = True
    if userCheck:
        await ctx.send(f"{ctx.author.mention} has already been initialized.")
    else:
        done = sf.addUser(botUser)
        if done:
            await ctx.send(f"{ctx.author.mention} has been initialized as a User.")
    print("init command :", botUser.name)

@client.command()
async def input(ctx):
    await ctx.message.delete()
    today = date.today()
    dateRecord = sf.checkRecord(ctx.author.id);
    if dateRecord:
        await ctx.send(f"Input already recorded today as '{dateRecord}'. Use *edit command to edit")
        return
    else:
        embed = discord.Embed(
            title = f"Enter the values for {today}",
            description ="||This request will timeout in 2 minuites||",
            colour = discord.Colour.orange())
        sent = await ctx.send(embed = embed)
        def check(m):
            if(ctx.author == m.author and m.channel == ctx.channel):
                return True
        try:
            msg = await client.wait_for("message", timeout = 120, check = check)
            if msg:
                await sent.delete()
                await msg.delete()
                m = msg.content

                def charCheck(s):
                    for i in s:
                        if(i != 'y' and i != 'n'):
                            return False
                    return True
                if(len(m)<=5 and charCheck(m)):
                    sf.inputData(ctx.author.id, m)
                    print(f"input updated : {m}")
                    await ctx.send(f"Input from {ctx.author.name} recorded as '{m}' for {today}. Very Naice")
                else:
                    await ctx.send("Invalid input, type *input to try again")
        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send("Cancelling due to timeout",delete_after=10)

@client.command()
async def edit(ctx):
    await ctx.message.delete()
    today = date.today()
    embed = discord.Embed(
        title = f"Enter the edited values for {today}",
        description ="||This request will timeout in 2 minuites||",
        colour = discord.Colour.orange())
    sent = await ctx.send(embed = embed)
    def check(m):
        if(ctx.author == m.author and m.channel == ctx.channel):
            return True
    try:
        msg = await client.wait_for("message", timeout = 120, check = check)
        if msg:
            await sent.delete()
            await msg.delete()
            m = msg.content
            def charCheck(s):
                for i in s:
                    if(i != 'y' and i != 'n'):
                        return False
                return True
            if(len(m)<=5 and charCheck(m)):
                record = sf.checkRecord(ctx.author.id)
                if not record:
                    await ctx.send("No original input, use *input.")
                    return
                sf.editData(ctx.author.id, m)
                await ctx.send(f"Input changed by {ctx.author.name} from '{record}' to '{m}' for {today}. Very Naice")
            else:
                await ctx.send("Invalid input, type *input to try again")
    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send("Cancelling due to timeout",delete_after=10)
@client.command()
async def viewmine(ctx):
    rawData = sf.retriveData(ctx.author.id)
    viewList = sf.calculateData(rawData)
    if not viewList:
        await ctx.send("No data to view")
    embed=discord.Embed(title="User-Scores", colour = discord.Colour.orange())
    embed.add_field(name = "Data", value = """
    Paid Attention:  
    Zoned Out:
    Current Streak:  
    Highest Streak:
    Recent Record:  
    """, inline=True)
    embed.add_field(name=f"{ctx.author.name}", value=f"""
    {viewList[0]}
    {viewList[1]}
    {viewList[2]}
    {viewList[3]}
    {viewList[4]}
    """, inline=True) 
    await ctx.send(embed=embed)


@client.command()
async def view(ctx):
    embed=discord.Embed(title="User-Scores", colour = discord.Colour.orange())
    embed.add_field(name = "Data", value = """
    Paid Attention:  
    Zoned Out:
    Current Streak:  
    Highest Streak:
    Recent Record:  
    """, inline=True)
    users = sf.getUsers()
    for i in users:
        rawData = sf.retriveData(i)
        viewList = sf.calculateData(rawData)
        embed.add_field(name=f"{sf.getUsername(i)}", value=f"""
        {viewList[0]}
        {viewList[1]}
        {viewList[2]}
        {viewList[3]}
        {viewList[4]}
        """, inline=True) 

    embed.set_footer(text="ggwp")
    await ctx.send(embed=embed)

@client.command()
async def viewall(ctx):
    
    for user in sf.getUsers():
        embed = discord.Embed(title = f"{sf.getUsername(user)}'s record", colour = discord.Colour.orange())
        data = sf.retriveData(user)
        for i in data.keys():
            embed.add_field(name = f"{i}", value = f"{data[i]}", inline=False)
        await ctx.send(embed=embed)

client.run("ODc0Mjk4MDQ0MDg1MDU5NTk0.YRE7gQ._I44cEpJCRwBxxfDbUB42L4GfPQ")
