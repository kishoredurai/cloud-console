import pyrebase
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for,Response
from flask_mysqldb import MySQL
from authlib.integrations.flask_client import OAuth
import re

import MySQLdb.cursors

app = Flask(__name__)  # Initialze flask constructor
mysql = MySQL(app)
oauth = OAuth(app)


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_console'


#google Login 
app.config['SECRET_KEY'] = "THIS SHOULD BE SECRET"
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






# initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

# Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": "" , "contact": "" , "user_type": "" , "rollno": "" , "dept": "","user_id":"" , "user_profile" : ""}


# Login


@app.route("/")
def login():
    #return render_template("Student/student_home.html")
    if person["is_logged_in"] == True:
        if(person["user_type"] == 'provider'):
            return redirect(url_for('welcome'))
        elif(person["user_type"] == 'student'):
            return redirect(url_for('home'))
    else:
        return render_template("login.html")


#Google Login

@app.route('/login/google')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/login/google/authorize')
def google_authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo').json()
    email=resp["email"]
    name=resp["given_name"]
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user where email_id=%s LIMIT 1',[email])
    student = cursor.fetchone()
    print(student)
    if(student):
        global person
        person["is_logged_in"] = True
        person["email"] = resp["email"]
        person["name"] = student['name']
        person["user_type"] = 'student'
        person["dept"] = student['department']

        person["rollno"] = student['rollno']
        person["user_id"] = student['user_id']

        person["contact"] = student['mobile']

        person["user_profile"] = resp["picture"]
            
        #return redirect(url_for('login'))
        return redirect(url_for('home'))

    else:
        text = resp["email"]
        result = re.split(r"\.", text)
        a=result[1][:2]
        if(a=="cs"):
            a="COMPUTER SCIENCE AND ENGINEERING"
        if(a=="ct"):
             a="COMPUTER TECHNOLOGY"
        print((result[1][:2]))
        return render_template("Student/student_register.html",student=resp,a=a)


    # return render_template('edit.html',resp=resp,a=a)
    return redirect(url_for('login'))







#Student Register


@app.route("/student/registe", methods=["POST", "GET"])
def registe():

    if request.method == "POST":
        result = request.form
        email = result["email"]
        rollno = result["rollno"]
        name = result["name"]
        contact = result["contact"]
        dept = result["dept"]
        profile = result["profile"]
       
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('insert into user(name,rollno,department,email_id,mobile,user_profile,db_password,user_type) values(%s,%s,%s,%s,%s,%s,%s,"student")', [name,rollno,dept,email,contact,profile,rollno])
        mysql.connection.commit()

        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

    if person["is_logged_in"] == True and person["user_type"] == 'provider':
       return render_template("profile.html", email=person["email"], name=person["name"],contact=person["contact"])

    else:
        return redirect(url_for('login'))

   
@app.route("/home")
def home():
        return render_template("Student/student_home.html",stu=person)




@app.route("/provider/profile")
def profile():
    if person["is_logged_in"] == True and person["user_type"] == 'provider':

       return render_template("profile.html", email=person["email"], name=person["name"],contact=person["contact"])

    else:
        return redirect(url_for('login'))






# Sign up/ Register


@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":  # Only if data has been posted
        result = request.form  # Get the data
        email = result["email"]
        password = result["pass"]
        try:
            # Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            # Insert the user data in the global person
            
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            
            # Get the name of the user
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            person["contact"] = data.val()[person["uid"]]["contact"]
            person["user_type"] = data.val()[person["uid"]]["user_type"]

            if(person["user_type"] == 'provider'):
                return redirect(url_for('welcome'))
            else:
                return Response("<h1> Admin</h1>")
      
        except:
            print("logout")
            # If there is any error, redirect back to login
            return redirect(url_for('login'))
    else:
        if person["is_logged_in"] == True and person["user_type"] == 'provider':
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))



@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/database")
def database():
    if person["is_logged_in"] == True and person["user_type"] == 'provider':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM database_users,user where database_users.user_id = user.user_id')
        account = cursor.fetchall()
        return render_template("database.html", email=person["email"], name=person["name"], value=account)

    else:
        return redirect(url_for('login'))




# Welcome page


@app.route("/welcome")
def welcome():
    if person["is_logged_in"] == True and person["user_type"]=='provider':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        account=cursor.execute('SELECT COUNT(*) FROM database_users')
        print(account)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sas=cursor.execute('SELECT COUNT(*) FROM database_users where db_status="Active"')
        print(sas)
        return render_template("welcome.html", email=person["email"], name=person["name"],data=account,ac=sas)

    else:
        return redirect(url_for('login'))





@app.route("/sas", methods=["POST", "GET"])
def sas():
    if request.method == "POST":
        if request.form.get("submit_b"):
            result = request.form  # Get the data
            ss = result["submit_b"]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('update database_users set db_status = "Active" , Request_status = "Accepted"  where db_id=%s;', [ss])
            mysql.connection.commit()            
            return Response("<h1>"+ss+"</h1>")

        if request.form.get("submit_a"):
            result = request.form  # Get the data
            ss = result["submit_a"]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('update database_users set db_status = "Deactive" , Request_status = "Rejected" where db_id=%s;', [ss])
            mysql.connection.commit()            
            return Response("<h1> decline :"+ss+"</h1>")

        # if request.form.get("submit_a"):
        #     result = request.form  # Get the data
        #     ss = result["submit_a"]
        #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #     cursor.execute('update database_users set db_status = "Deactive" , Request_status = "Decline" where db_id=%s;', [ss])
        #     mysql.connection.commit()            
        #     return Response("<h1> decline :"+ss+"</h1>")

        






# Welcome page
@app.route("/logout")
def logout():
    person["is_logged_in"] = False
    return redirect(url_for('login'))

# If someone clicks on login, they are redirected to /result


# If someone clicks on register, they are redirected to /register


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":  # Only listen to POST
        result = request.form  # Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        contact = result["cont"]
        try:
            # Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            # Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            # Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            print(email, password,contact)
            # Append data to the firebase realtime database
            data = {"name": name, "email": email, "contact": contact}
            db.child("users").child(person["uid"]).set(data)
            # Go to welcome page
            return redirect(url_for('welcome'))
        except:
            # If there is any error, redirect to register
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))

    # return Response("<h1>Success!</h1>")




###### Student Login  #########

@app.route("/profile", methods=["POST", "GET"])
def student_profile():

    if person["is_logged_in"] == True and person["user_type"] == 'student':
        
        if request.method == "POST":
            if request.form.get("update"):
                result = request.form  # Get the data
                ss = result["dbpasswd"]
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('update user set db_password=%s where user_id=%s;', [ss,person['user_id']])
                mysql.connection.commit()            
                return redirect(url_for('profile'))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user where user_id = %s',[person['user_id']])
        student = cursor.fetchone()
        return render_template("Student/student_profile.html", user=person , password=student['db_password'])

    else:
        return redirect(url_for('login'))

@app.route("/student_database")
def student_database():
    if person["is_logged_in"] == True and person["user_type"] == 'student':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM database_users where user_id = %s',[person['user_id']])
        account = cursor.fetchall()
        return render_template("Student/student_database.html",value=account,user=person)

    else:
        return redirect(url_for('login'))

    
@app.route("/db_register", methods=["POST", "GET"])
def registers():
    
    if request.method == "POST":

        result = request.form   
        software = result["database"]
        start_date = result["startdate"]
        end_date = result["enddate"]
        
        dbname = result["dbname"]
        remark = result["remark"]

        status = "Not Approved"


        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('insert into database_users(user_id, db_software, start_date, end_date, db_name, Request_status, user_remark) values(%s,%s,%s,%s,%s,%s,%s)', [
                       person['user_id'],software,start_date,end_date, dbname, status, remark])
        mysql.connection.commit()
        return redirect(url_for('student_database'))
    return render_template("Student/student_db_register.html",user=person)



@app.route("/db_update", methods=["POST", "GET"])
def db_update():
    if request.method == "POST":
        if request.form.get("delete"):
            result = request.form  # Get the data
            ss = result["delete"]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('Delete from database_users where db_id=%s;', [ss])
            mysql.connection.commit()            
            return redirect(url_for('student_database'))

        if request.form.get("update"):
            result = request.form  # Get the data
            ss = result["update"]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM database_users where db_id=%s;',[ss])
            data = cursor.fetchone()           
            return render_template("Student/student_db_update.html",user=person,data=data)

       ###--- database update Form ----###
        result = request.form  # Get the data
        start_date = result["startdate"]
        end_date = result["enddate"]
        id = result["id"]
        dbname = result["dbname"]
        remark = result["remark"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('update database_users set start_date=%s ,end_date=%s,db_name=%s,user_remark=%s where db_id=%s;',[start_date,end_date,dbname,remark,id])
        mysql.connection.commit()
        return redirect(url_for('student_database'))
