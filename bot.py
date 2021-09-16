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

                    # for i in range(len(jsonFile['elements'])):
                    #     if(jsonFile['elements'][i]['user_id']==ctx.author.id):
                    #         jsonFile['elements'][i]['dataRecord'][f'{today}'] = f'{m}'
                    #         datajsonOut = open(r"./data.json", 'w')
                    #         datajsonOut.write(json.dumps(jsonFile))
                    #         datajsonOut.close()
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
    datajson = open(r"./data.json", 'r')
    jsonFile = json.loads(datajson.read())
    datajson.close()
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
                for i in range(len(jsonFile['elements'])):
                    if(jsonFile['elements'][i]['user_id']==ctx.author.id):
                        jsonFile['elements'][i]['dataRecord'][f'{today}'] = f'{m}'
                        datajsonOut = open(r"./data.json", 'w')
                        datajsonOut.write(json.dumps(jsonFile))
                        datajsonOut.close()
                        print(f"input updated : {jsonFile['elements'][i]}")
                        await ctx.send(f"Input changed by {ctx.author.name} to '{m}' for {today}. Very Naice")
            else:
                await ctx.send("Invalid input, type *input to try again")
    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send("Cancelling due to timeout",delete_after=10)

@client.command()
async def view(ctx):
    def yncount(user):
        totalstr = " "
        for i in user['dataRecord'].values():
            totalstr += i
        ycount = totalstr.count("y")
        ncount = totalstr.count("n")
        latestStreak = 0
        for i in range(len(totalstr)-1, 0, -1):
            if totalstr[i] == "y":
                latestStreak += 1
            elif(totalstr[i] == "n"):
                break

        current_streak=0
        biggest_streak=0
        for i in totalstr:
            if i=='y':
                current_streak+=1
            if(i=='n' or i==totalstr[len(totalstr)-1]):
                if current_streak>biggest_streak:
                    biggest_streak=current_streak
                    current_streak=0
        if(len(totalstr)<=10):
            lateststr = totalstr
        else:
            lateststr = totalstr[len(totalstr)-11:]
        return [ycount, ncount, latestStreak, biggest_streak, lateststr]

    datajson = open(r"./data.json", 'r')
    jsonFile = json.loads(datajson.read())
    datajson.close()
    infodict = {}
    for element in jsonFile['elements']:
        if(len(element['dataRecord'])==0):
            await ctx.send(f"No inputs available to display for {element['name']}")
        infodict[f"{element['name']}"] = yncount(element)
    embed=discord.Embed(title="User-Scores", colour = discord.Colour.orange())
    embed.add_field(name = "Data", value = """
    Paid Attention:  
    Zoned Out:
    Current Streak:  
    Highest Streak:
    Recent Record:  
    """, inline=True)
    for i in infodict.keys():
        embed.add_field(name=f"{i}", value=f"""
        {infodict[i][0]}
        {infodict[i][1]}
        {infodict[i][2]}
        {infodict[i][3]}
        {infodict[i][4]}
        """, inline=True) 

    embed.set_footer(text="ggwp")
    await ctx.send(embed=embed)

@client.command()
async def viewall(ctx):
    datajson = open(r"./data.json", 'r')
    jsonFile = json.loads(datajson.read())
    datajson.close()
    for user in jsonFile['elements']:
        embed = discord.Embed(title = f"{user['name']}'s record", colour = discord.Colour.orange())
        for i in user['dataRecord'].keys():
            embed.add_field(name = f"{i}", value = f"{user['dataRecord'][i]}", inline=False)
        await ctx.send(embed=embed)

client.run("ODc0Mjk4MDQ0MDg1MDU5NTk0.YRE7gQ._I44cEpJCRwBxxfDbUB42L4GfPQ")
