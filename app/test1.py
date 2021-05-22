# import psycopg2


# conn = psycopg2.connect(database="test", user = "test", password = "kishore", host = "127.0.0.1", port = "5432")
# a="sample"

# cur = conn.cursor()
# sqlCreateDB = "create database "+a+";"
# cur.execute(sqlCreateDB)


import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE

con = psycopg2.connect(dbname='postgres',user='postgres', host='127.0.0.1',password='kishore',port='5432')

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE

cur = con.cursor()
a='192CT120'
db='usertable'
b="sass"
# # cur.execute(sql.SQL("CREATE DATABASE {}").format(
# #         sql.Identifier(db))
# #     )

# # query = "CREATE ROLE "'"'+a+'"'" LOGIN PASSWORD '"+a+"';"
# # cur.execute(sql.SQL(query).format())


# # query = "GRANT ALL PRIVILEGES ON DATABASE "+db+" to "'"'+a+'"'";"
# # cur.execute(sql.SQL(query).format())

# query = "REVOKE ALL PRIVILEGES ON DATABASE "+db+" FROM "'"'+a+'"'";" 
# cur.execute(sql.SQL(query).format())
# query = "REVOKE CONNECT ON DATABASE "+db+" FROM "'"'+a+'"'";" 
# cur.execute(sql.SQL(query).format())
ss = "ALTER USER "'"'+a+'"'" WITH PASSWORD '"+b+"' ;"
cur.execute(sql.SQL(ss).format())
