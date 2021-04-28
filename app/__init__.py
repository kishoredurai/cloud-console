from flask import Flask, flash, redirect, render_template, request, session, abort, url_for,Response    
from flask_mysqldb import MySQL
from datetime import date

from apscheduler.schedulers.background import BackgroundScheduler

from authlib.integrations.flask_client import OAuth
import re
import pyrebase
import schedule
import time,atexit

import MySQLdb.cursors

app = Flask(__name__)  # Initialze flask constructor
mysql = MySQL(app)
oauth = OAuth(app)


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_console'


#google Login 
app.config['SECRET_KEY'] = "7VwoqYbf3cVOiHu_wWtb_A"
app.config['GOOGLE_CLIENT_ID'] = "642500080555-7aaod8odtsdktfu7dusperbktfu0slc6.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET'] = "TsUtxn9Y-dqW1M_K6zGjdYR1"





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



    
# Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": "" , "contact": "" , "user_type": "" , "rollno": "" , "dept": "","user_id":"" , "user_profile" : ""}






###################### db create funciton ##############################

def SQL_privilleges(data):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)    
    try:
        sqlCreateUser = "GRANT ALL PRIVILEGES ON %s.* TO '%s'@'localhost' IDENTIFIED BY '%s';"%(data['db_name'],data['rollno'],data['db_password'])
        cursor.execute(sqlCreateUser)
        print('grant privileges')
    except Exception as Ex:
        print("Error creating MySQL User: %s"%(Ex))









################################ timer ##############


def database_check():
    db = MySQLdb.connect("127.0.0.1","root","","db_console",cursorclass=MySQLdb.cursors.DictCursor)
    cursor = db.cursor()
    
    today = date.today()
    print(today)
    cursor.execute('SELECT * FROM database_users,user where database_users.user_id=user.user_id and database_users.db_status="Deactive" and database_users.Request_status = "Approved" and start_date = %s',[today,])
    data = cursor.fetchall() 
    if data :
        for x in range(len(data)):

            name=data[x]['db_name']              
            try:
                sqlCreateUser = "GRANT ALL PRIVILEGES ON %s.* TO '%s'@'localhost' IDENTIFIED BY '%s';"%(data[x]['db_name'],data[x]['rollno'],data[x]['db_password'])
                cursor.execute(sqlCreateUser)
                print('approved')
            except Exception as Ex:
                print("Error creating MySQL User: %s"%(Ex))

            cursor.execute('update database_users set db_status = "Active"  where db_id=%s;', [data[x]['db_id']])
            db.commit()
    else:
        print('no details')
def provider_email():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

scheduler = BackgroundScheduler()
scheduler.add_job(func=database_check, trigger="interval", hours=4)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())



#### default function ###########

def email():
    print('testing')






from app.code import login,codes,user,provider