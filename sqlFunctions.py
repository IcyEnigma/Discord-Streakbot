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

def checkRecord(user):
    today = date.today()
    today = str(today).replace("-","_")
    try:
        cursor.execute(f'''SELECT "{today}" FROM "public"."userTable" WHERE "userid" = '{user.id}';''')
    except psycopg2.errors.UndefinedColumn:
        print("NO ENTRY")
        return False
    if(cursor.rowcount == 0):
        return False
    resList =  cursor.fetchall()
    final = []
    for i in resList:
        final.append(i[0])
    print(final)
    return final
