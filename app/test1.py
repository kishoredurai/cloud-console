# import psycopg2


# conn = psycopg2.connect(database="test", user = "test", password = "kishore", host = "127.0.0.1", port = "5432")
# a="sample"

# cur = conn.cursor()
# sqlCreateDB = "create database "+a+";"
# cur.execute(sqlCreateDB)


import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE

con = psycopg2.connect(dbname='test',user='test', host='127.0.0.1',password='kishore',port='5432')

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE

cur = con.cursor()
a='kishore'
db='sample'
# cur.execute(sql.SQL("CREATE DATABASE {}").format(
#         sql.Identifier(db))
#     )

cur.execute(sql.SQL("CREATE USER {username} WITH PASSWORD '{password}'").format(
        username=sql.Identifier(a),
        password=sql.Identifier(a)    
    ))


# cur.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {databasename} to {username};").format(
#         databasename=sql.Identifier(db),
#         username=sql.Identifier(a)    
#     ))