import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
conn = psycopg2.connect(database="test", user = "test", password = "kishore", host = "127.0.0.1", port = "5432")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)




cur = conn.cursor()

a="192CT120"

cur.execute("CREATE DATABASE "+a+";")


conn.commit()