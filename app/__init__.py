from flask import Flask, flash, redirect, render_template, request, session, abort, url_for,Response,jsonify, json
from flask_mysqldb import MySQL
from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler

from authlib.integrations.flask_client import OAuth
import re
import pyrebase
import schedule
import time,atexit
import os
import MySQLdb.cursors

## mail sender
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64


#Postegsql
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


app = Flask(__name__)  # Initialze flask constructor
mysql = MySQL(app)
oauth = OAuth(app)


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_console'


#google Login 
app.config['SECRET_KEY'] = "7VwoqYbf3cVOiHu_wWtb_A"
app.config['GOOGLE_CLIENT_ID'] = "91281671272-rrve31v6ghn9afjfhga5l9s85t9saroq.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET'] = "ZcVSybDQ8RnczOjFbdJeWPdL"





google = oauth.register(
    name = 'google',
    client_id = app.config["GOOGLE_CLIENT_ID"],
    client_secret = app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs = {'scope': 'openid email profile'},
)



# Add your own details
config = {
    "apiKey": "AIzaSyDCL31T4QStQlXNtxBF7GHpZqljSRh_h-M",
    "authDomain": "db-console.firebaseapp.com",
    "databaseURL": "https://db-console-default-rtdb.firebaseio.com",
    "projectId": "db-console",
    "storageBucket": "db-console.appspot.com",
    "messagingSenderId": "91281671272",
    "appId": "1:91281671272:web:f97ee0cd7f4ecc508ce7dd"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


conn = psycopg2.connect(dbname='postgres',user='postgres', host='127.0.0.1',password='kishore',port='5432')
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

db = MySQLdb.connect("127.0.0.1","root","","db_console",cursorclass=MySQLdb.cursors.DictCursor)


# Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": "" , "contact": "" , "user_type": "" , "rollno": "" , "dept": "","user_id":"" , "user_profile" : "", "user" : "" ,"console":""}





###################### db create funciton ##############################










#### default Email function ###########

def email(sender,messages,subject):

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = 'cloud@bitsathy.ac.in'
    message["To"] = sender

    html = """\
    <html>
    <body>
        <p>Hi,<br>
        How are you?<br>
        <a href="http://www.realpython.com">Real Python</a> 
        has many great tutorials.
        </p>
    </body>
    </html>
    """

   
    part2 = MIMEText(html, "html")

    # message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login('cloud@bitsathy.ac.in', 'Cloud@987')
        server.sendmail(
            'cloud@bitsathy.ac.in', sender, message.as_string()
        )
    print('mail sent')
   



################################ Database Check #######################



def database_check():
    cursor = db.cursor()
    today = date.today()
    cursor.execute('SELECT * FROM database_users,user where database_users.user_id=user.user_id and database_users.db_status="Deactive" and database_users.Request_status = "Approved" and start_date = %s',[today,])
    data = cursor.fetchall() 
    if data :
        for x in range(len(data)):

            if(data[x]['db_software']=='SQL'):
                Sql_db_allow(data[x])
            elif(data[x]['db_software']=='PostgreSQL'):
                Postegsql_db_allow(data[x])
                print('poste')
    else:
        print('add no details')

    # revoke permission
    cursor.execute('SELECT * FROM database_users,user where database_users.user_id=user.user_id and database_users.db_status="Active" and database_users.Request_status = "Approved" and end_date = %s',[today,])
    data = cursor.fetchall() 
    if data :
        for x in range(len(data)):
            if(data[x]['db_software']=='SQL'):
                Sql_db_remove(data[x])
            elif(data[x]['db_software']=='PostgreSQL'):
                Postegsql_db_remove(data[x])
    else:
        print('revoke no details')


################################ SQL prvilleges and revoke #######################



def Sql_db_allow(data):
    cursor = db.cursor()
    name=data['db_name']              
    try:
        sqlCreateUser = "GRANT ALL PRIVILEGES ON %s.* TO '%s'@'localhost' IDENTIFIED BY '%s';"%(data['db_name'],data['rollno'],data['db_password'])
        cursor.execute(sqlCreateUser)
        print('approved'+name)
        cursor.execute('update database_users set db_status = "Active"  where db_id=%s;', [data['db_id']])
        db.commit()
    except Exception as Ex:
        print('sql allow')
        print("Error creating MySQL User: %s"%(Ex))

def Sql_db_remove(data):
    cursor = db.cursor()
    name=data['db_name']              
    try:
        sqlCreateUser = "REVOKE ALL PRIVILEGES ON %s.* FROM '%s'@'localhost';"%(data['db_name'],data['rollno'])
        cursor.execute(sqlCreateUser)    
        print('REVOKED '+name)
        cursor.execute('update database_users set db_status = "Deactive"  where db_id=%s;', [data['db_id']])
        db.commit()
    except Exception as Ex:
        print('sql remove')
        print("Error creating MySQL User: %s"%(Ex))

            
    

################################ Postegsql prvilleges and revoke #######################


def Postegsql_db_allow(data):
    cur = conn.cursor()
    cursor = db.cursor()
    name=data['db_name']              
    try:
        query = "GRANT ALL PRIVILEGES ON DATABASE "+data['db_name']+" to "'"'+data['rollno']+'"'";"
        cur.execute(sql.SQL(query).format())
        print('postge approved '+name)
        cursor.execute('update database_users set db_status = "Active"  where db_id=%s;', [data['db_id']])
        db.commit()
    except Exception as Ex:
        print("Error creating poss User: %s"%(Ex))

            
def Postegsql_db_remove(data): 
    cur = conn.cursor()

    cursor = db.cursor()
    name=data['db_name']              
    try:
        query = "REVOKE ALL PRIVILEGES ON DATABASE "+data['db_name']+" FROM "'"'+data['rollno']+'"'";" 
        cur.execute(sql.SQL(query).format())
        query = "REVOKE CONNECT ON DATABASE "+data['db_name']+" FROM "'"'+data['rollno']+'"'";" 
        cur.execute(sql.SQL(query).format())
        print('REVOKED '+name)
        cursor.execute('update database_users set db_status = "Deactive"  where db_id=%s;', [data['db_id']])
        db.commit()
    except Exception as Ex:
        print("Error posteges remove User: %s"%(Ex))
   





####################### provider and admin db create and privilleges ############################




def SQL_db_create_check(db_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)    
    cursor.execute('SELECT * FROM database_users,user where database_users.user_id=user.user_id and database_users.db_id=%s',[db_id])
    data = cursor.fetchone() 
    cursor.execute('SELECT * FROM mysql.user where user=%s',[data['rollno']])
    datas = cursor.fetchall()
    if not datas:
        try:
            sqlCreateUser = "CREATE USER '%s'@'localhost' IDENTIFIED BY '%s';"%(data['rollno'],data['rollno'])
            cursor.execute(sqlCreateUser)
            cursor.execute('update db_login_user set db_user_status = "Active" and where db_software = "SQL" and db_id=%s;',[data['user_id']])
            mysql.connection.commit() 
        except Exception as Ex:
            print("Error creating MySQL User: %s"%(Ex))   

    ## Database create ##
    try:
        sqlCreateUser = "CREATE DATABASE %s;"%(data['db_name'])
        cursor.execute(sqlCreateUser)
        print('db created')
    except Exception as Ex:
        print("Error creating MySQL User: %s"%(Ex))
    
    email(data['email_id'],'Account Created','sql db created')

    ## check database create date

    today = date.today()
    if(data["start_date"] <= today):

        print("created")
        SQL_privilleges(data)
        cursor.execute('update database_users set db_status = "Active" , Request_status = "Approved" where db_id=%s;', [db_id])
        mysql.connection.commit()  
    else:
        print("not created") 
        cursor.execute('update database_users set db_status = "Deactive" , Request_status = "Approved" where db_id=%s;', [db_id])
        mysql.connection.commit() 
    



def postgre_db_create_check(db_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
    cur = conn.cursor()   
    cursor.execute('SELECT * FROM database_users,user where database_users.user_id=user.user_id and database_users.db_id=%s',[db_id])
    data = cursor.fetchone() 
    cur.execute('SELECT usename FROM pg_catalog.pg_user where usename = %s',[data['rollno']])
    datas = cur.fetchone()
    if not datas:
        try:
            query = "CREATE USER "'"'+data['rollno']+'"'" LOGIN PASSWORD '"+data['rollno']+"';"
            cur.execute(sql.SQL(query).format())
            cursor.execute('update db_login_user set db_user_status = "Active" and where db_software = "PostgreSQL" and db_id=%s;',[data['user_id']])
            mysql.connection.commit() 
        except Exception as Ex:
            print("Error creating MySQL User: %s"%(Ex))   

    ## Database create ##
    try:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(data['db_name'])))
        print('db created')
    except Exception as Ex:
        print("Error creating MySQL User: %s"%(Ex))
    
    email(data['email_id'],'Account Created','Posteges sql')
    ## check database create date

    today = date.today()
    if(data["start_date"] <= today):

        print("created")
        postgre_privilleges(data)
        cursor.execute('update database_users set db_status = "Active" , Request_status = "Approved" where db_id=%s;', [db_id])
        mysql.connection.commit()  
    else:
        print("not created") 
        cursor.execute('update database_users set db_status = "Deactive" , Request_status = "Approved" where db_id=%s;', [db_id])
        mysql.connection.commit() 








############################  Database Privileges  #####################################


def SQL_privilleges(data):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM db_login_user where db_software = "SQL" and user_id=%s',[data['user_id']])
    db_user_detail = cursor.fetchone()    
    try:
        sqlCreateUser = "GRANT ALL PRIVILEGES ON %s.* TO '%s'@'localhost' IDENTIFIED BY '%s';"%(data['db_name'],data['rollno'],db_user_detail['user_id'])
        cursor.execute(sqlCreateUser)
        print('grant privileges')
    except Exception as Ex:
        print("Error creating MySQL User: %s"%(Ex))


def postgre_privilleges(data):
    cur = conn.cursor()
    try:
        query = "GRANT ALL PRIVILEGES ON DATABASE "+data['db_name']+" to "'"'+data['rollno']+'"'";"
        cur.execute(sql.SQL(query).format())
        
        print('grant privileges')
    except Exception as Ex:
        print("Error creating postgre User: %s"%(Ex))










######################## Daily Mail send ##########################

def provider_email():

    email('kishore.ct19@bitsathy.ac.in','this test mail','daily status')



##################### timmer #######################################

scheduler = BackgroundScheduler()
scheduler.add_job(func=provider_email, trigger="interval", hours=12)
scheduler.add_job(func=database_check, trigger="interval", hours=2)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())






from app.code import login,codes,user,provider,admin