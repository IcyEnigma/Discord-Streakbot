# import os
# import urllib.parse as up
# import psycopg2

# up.uses_netloc.append("postgres")
# url = up.urlparse(os.environ["postgres://hohnpdua:d93cg63E-CWeTLRWysWrHZ-RCXfmpx4K@john.db.elephantsql.com/hohnpdua"])
# conn = psycopg2.connect(
# database="hohnpdua",
# user="hohnpdua",
# password="d93cg63E-CWeTLRWysWrHZ-RCXfmpx4K",
# host=url.hostname,
# port=url.port
# )

import os
import urllib.parse as up
import psycopg2

up.uses_netloc.append("postgres")
os.environ['DATABASE_URL'] = "postgres://hohnpdua:d93cg63E-CWeTLRWysWrHZ-RCXfmpx4K@john.db.elephantsql.com/hohnpdua"
url = up.urlparse(os.environ['DATABASE_URL'])
conn = psycopg2.connect(database=url.path[1:],
user=url.username,
password=url.password,
host=url.hostname,
port=url.port
)

