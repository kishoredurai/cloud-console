from app import *


@app.route("/")
def login():
    #return render_template("Student/student_home.html")
    if(not session.get("id") is None):
        if(person["user"] == 'student'):
            return redirect(url_for('home'))
        elif(person["user"] == 'provider'):
            return redirect(url_for('provider_home'))
        else:
            session.pop("id", None)
            return redirect(url_for('login'))
    else:
        return render_template("login.html")


#Google Login
@app.route('/login/google')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    if not session.get("id") is None and person["user"] == 'student':
        return redirect(url_for('home'))
    return google.authorize_redirect(redirect_uri)
    


@app.route('/login/google/authorize')
def google_authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo').json()

    
    email=resp["email"]    
    # name=resp["given_name"]


    #  check domain name

    domain = email.split('@')[1]
    if(domain=='bitsathy.ac.in'):

        print(domain)
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user where email_id=%s and account_status="yes"  LIMIT 1',[email])
        student = cursor.fetchone()
        #print(student)
    
  
        if(student):
        
            global person
            session["id"] = student['user_id']
            person["user"] = "student"
            person["user_type"] = student["user_type"]
            person["email"] = resp["email"]
            person["name"] = student['name']
            person["dept"] = student['department']
            person["rollno"] = student['rollno']
            person["user_id"] = student['user_id']
            person["contact"] = student['mobile']
            person["user_profile"] = resp["picture"]


            cursor.execute('insert into login_history(user_id) values(%s)', [student['user_id']])
            mysql.connection.commit()

            ## ascii convertion base64
            message = student['rollno']
            message_bytes = message.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            base64_message = base64_bytes.decode('ascii')

            person["console"] = base64_message

            #flash("Password length must be at least 10 characters")
            #return redirect(url_for('login'))    
            #return red irect(url_for('login'))
            return redirect(url_for('home'))

        else:

            text = resp["email"]
            result = re.split(r"\.", text)
            a=result[1][:2]
            print((result[1][:2]))
            if(a == 'ac'):
                print('entered')
                
                person['email']=resp['email']
                person['name']=resp['name']
                person['user_profile']=resp['picture']
                person["user_type"] = 'staff'
                
                return redirect(url_for('student_register'))
                #return render_template("Student/student_register.html",student=resp,dept=account,user='staff')
                #student_register(resp,account,'student')
            else:
                cursor.execute('SELECT * FROM department where department_code=%s LIMIT 1',[a])
                data = cursor.fetchone()     
                sds=data['department_name']        
                #return redirect(url_for('student_register'))
                return render_template("Student/student_register.html",student=resp,dept=data['department_name'],user='student')
                #return redirect(url_for('login'),resp,data['department_name'],'student')
    

    if not session.get("id") is None and person["user"] == 'student':
        return redirect(url_for('home'))

    # return render_template('edit.html',resp=resp,a=a)
    return redirect(url_for('login'))



@app.route("/logout")
def logout():
    person.clear()
    session.pop("id", None)
    return redirect(url_for('login'))


@app.route("/login", methods=["POST", "GET"])
def result():
    if request.method == "POST":  # Only if data has been posted
        result = request.form  # Get the data
        email = result["email"]
        password = result["pass"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        message = password
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')

        cursor.execute('SELECT * FROM admin where admin_username=%s and admin_password=%s LIMIT 1',[email,base64_message])
        student = cursor.fetchone()

        print("created")
        if(student):    
            print('entered')
            global person
            session["id"] = student['admin_id']
            person["email"] = student["admin_username"]
            person["name"] = student['admin_name']
            person["user"] = student['admin_user_type']
            person["user_id"] = student['admin_id']
            if(person["user"] == 'provider'):
                return redirect(url_for('provider_home'))
            elif(person["user"] == 'admin'):
                print('admin')
                return redirect(url_for('admin_home'))
      
        else:
            flash("Invalid password and Username")  
            # If there is any error, redirect back to login
            return redirect(url_for('login'))
    else:
        if not session.get("id") is None and person["user"] == 'provider':
            return redirect(url_for('provider_home'))
        else:
            return redirect(url_for('login'))



@app.route("/register", methods=["POST", "GET"])
def student_register():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if(person['user_type']=='staff'):        
        cursor.execute('SELECT * FROM department')
        account = cursor.fetchall()
        print(account)
        return render_template("Student/student_register.html",student=person,dept=account,user='staff')
    else:
        if not session.get("id") is None and person["user"] == 'provider':
            return redirect(url_for('provider_home'))
        else:
            return redirect(url_for('login'))




@app.route("/student/register", methods=["POST", "GET"])
def registe():

    if request.method == "POST":
        
        result = request.form
        email = result["email"]
        rollno = result["rollno"]
        name = result["name"]
        contact = result["contact"]
        dept = result["dept"]
        profile = result["profile"]
        user = result["user_type"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('insert into user(name,rollno,department,email_id,mobile,user_profile,db_password,user_type) values(%s,%s,%s,%s,%s,%s,%s,%s)', [name,rollno.upper(),dept,email,contact,profile,rollno.upper(),user])
        mysql.connection.commit()
        last_id=cursor.lastrowid

        #create linux user
        os.system("echo 2709 | sudo -S useradd -m -d /var/www/html/"+rollno.upper()+" -s /bin/bash -p $(echo "+rollno.upper()+" | openssl passwd -1 -stdin) "+rollno.upper())
                
        cursor.execute('insert into db_login_user(user_id,db_software,db_password) values(%s,%s,%s)', [last_id,'SQL',rollno.upper()])
        mysql.connection.commit()

        cursor.execute('insert into db_login_user(user_id,db_software,db_password) values(%s,%s,%s)', [last_id,'PostgreSQL',rollno.upper()])
        mysql.connection.commit()


        print('done')
        return redirect(url_for('login'))
    else:
        print('no post')
        return redirect(url_for('login'))
    
    if not session.get("id") is None and person["user"] == 'provider':
        return redirect(url_for('provider_home'))
    else:
        return redirect(url_for('login'))






@app.errorhandler(404)
def page_not_found(e):

    app.logger.info(f"Page not found: {request.url}")

    return redirect(url_for('login'))


