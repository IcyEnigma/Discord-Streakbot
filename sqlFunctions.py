import os
import urllib.parse as up
import psycopg2
from datetime import date

up.uses_netloc.append("postgres")
os.environ['DATABASE_URL'] = "postgres://hohnpdua:d93cg63E-CWeTLRWysWrHZ-RCXfmpx4K@john.db.elephantsql.com/hohnpdua"
url = up.urlparse(os.environ['DATABASE_URL'])
conn = psycopg2.connect(database=url.path[1:],
user=url.username,
password=url.password,
host=url.hostname,
port=url.port
)
cursor = conn.cursor()
today = str(date.today()).replace("-","_")

def getUsers():
    cursor.execute('''SELECT userid FROM "public"."userTable";''')
    resList =  cursor.fetchall()
    final = []
    for i in resList:
        final.append(i[0])
    return final

def addUser(user):
    cursor.execute('''INSERT INTO "public"."userTable" (userid,username) VALUES (%s,%s);''', (user.id,user.name))
    conn.commit()
    return True

def checkRecord(userid):
    try:
        cursor.execute(f'''SELECT "{today}" FROM "public"."userTable" WHERE "userid" = '{userid}';''')
    except psycopg2.errors.UndefinedColumn:
        return False
    fetchedData = cursor.fetchall()
    if(str(fetchedData[0][0]) == "None"):
        return False
    final = fetchedData[0][0]
    return final

def getColumns():
    cursor.execute('''SELECT * FROM "public"."userTable";''')
    desc = str(cursor.description)
    parseList = desc.split(",")
    colList = []
    start = False
    end = False
    colFlag = True
    for i in parseList:
        for j in range(len(i)):
            if(i[j] == "'"):
                start = j
            if(start):
                break
        if colFlag:    
            print(i[start+1:end])
            colList.append(i[start+1:-1])
            colFlag = False
        else:
            colFlag = True

    return colList

def inputData(userid, data):
    colList = getColumns()
    if today not in colList:
        cursor.execute(f'''ALTER TABLE "public"."userTable" ADD COLUMN "{today}" varchar(10);''')
        conn.commit()
    cursor.execute(f'''SELECT "{today}" FROM "public"."userTable" WHERE "userid" = '{userid}';''')
    fetchedData = cursor.fetchall()
    if (str(fetchedData[0][0]) == "None"):
        cursor.execute(f'''UPDATE "public"."userTable" SET "{today}" = '{data}' WHERE "userid" = '{userid}';''')
        conn.commit()
        cursor.execute(f'''SELECT "{today}" FROM "public"."userTable" WHERE "userid" = '{userid}';''')
        print(f"data updated for {userid} as ",cursor.fetchall())
    
def editData(userid, data):
    colList = getColumns()
    if today not in colList:
        cursor.execute(f'''ALTER TABLE "public"."userTable" ADD COLUMN "{today}" varchar(10);''')
        conn.commit()
    cursor.execute(f'''UPDATE "public"."userTable" SET "{today}" = '{data}' WHERE "userid" = '{userid}';''')
    conn.commit()
    cursor.execute(f'''SELECT "{today}" FROM "public"."userTable" WHERE "userid" = '{userid}';''')
    print(f"data updated for {userid} as ",cursor.fetchall())


def retriveData(userid):
    cols = getColumns()
    data = {}
    for i in cols:
        if(i != "userid" and i != "username" and i != "maxstreak"):
            cursor.execute(f'''SELECT "{i}" FROM "public"."userTable" WHERE "userid" = '{userid}';''')
            data[i] = str(cursor.fetchall()[0][0])
    return data

def calculateData(data):
    maxstreak = 0
    attention = 0
    zonedOut = 0
    totalstr = ""
    for i in data.values():
        totalstr += i
    none = totalstr.find("None")
    if(none > -1):
        totalstr = totalstr[:none]
    if(len(totalstr) == 0):
        return False
    print("TOTAL STR = ", totalstr)
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
    for j in range(len(totalstr)):
        i = totalstr[j]
        if i=='y':
            current_streak+=1
        if(i=='n' or j == len(totalstr)-1):
            if current_streak>biggest_streak:
                biggest_streak=current_streak
                current_streak=0
    if(len(totalstr)<=10):
        lateststr = totalstr
    else:
        lateststr = totalstr[len(totalstr)-11:]
    return [ycount, ncount, latestStreak, biggest_streak, lateststr]

        