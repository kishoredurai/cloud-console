from app import  *

@app.route("/")
def login():
    #return render_template("Student/student_home.html")
    if(not session.get("id") is None):
        if(person["user_type"] == 'student'):
            return redirect(url_for('home'))
        elif(person["user_type"] == 'provider'):
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
        session["id"] = student['user_id']
        person["user_type"] = student['user_type']
        person["email"] = resp["email"]
        person["name"] = student['name']
        person["dept"] = student['department']
        person["rollno"] = student['rollno']
        person["user_id"] = student['user_id']
        person["contact"] = student['mobile']
        person["user_profile"] = resp["picture"]
        #flash("Password length must be at least 10 characters")
        #return redirect(url_for('login'))    
        #return red irect(url_for('login'))
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

@app.route("/logout")
def logout():
    session.pop("id", None)
    person["user_type"] = ''
    return redirect(url_for('login'))


@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":  # Only if data has been posted
        result = request.form  # Get the data
        email = result["email"]
        password = result["pass"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin where admin_username=%s and admin_password=%s LIMIT 1',[email,password])
        student = cursor.fetchone()
        if(student):
            # Try signing in the user with the given information
            #user = auth.sign_in_with_email_and_password(email, password)
            # Insert the user data in the global person
            
            global person
            session["id"] = student['admin_id']
            person["email"] = student["admin_username"]
            person["name"] = student['admin_name']
            person["user_type"] = student['admin_user_type']
            person["user_id"] = student['admin_id']
            if(person["user_type"] == 'provider'):
                return redirect(url_for('provider_home'))
            elif(person["user_type"] == 'admin'):
                return redirect(url_for('login'))
            else:
                return Response("<h1> Admin</h1>")
      
        else:
      
            # If there is any error, redirect back to login
            return redirect(url_for('login'))
    else:
        if not session.get("id") is None and person["user_type"] == 'provider':
            return redirect(url_for('provider_home'))
        else:
            return redirect(url_for('login'))



@app.errorhandler(404)
def page_not_found(e):

    app.logger.info(f"Page not found: {request.url}")

    return redirect(url_for('login'))