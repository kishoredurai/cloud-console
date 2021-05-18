from app import  *

@app.route("/home")
def home():
    if not session.get("id") is None and person["user"] == 'student':

        return render_template("Student/student_home.html",user=person)

    else:
        return redirect(url_for('login'))


@app.route("/profile", methods=["POST", "GET"])
def student_profile():
    if not session.get("id") is None and person["user"] == 'student':
               
        if request.method == "POST":
            if request.form.get("update"):
                result = request.form  # Get the data
                ss = result["dbpasswd"]
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                try:
                    sqlCreateUser = "ALTER USER '%s'@'localhost' IDENTIFIED BY '%s';"%(person['rollno'],ss)
                    cursor.execute(sqlCreateUser)
                    cursor.execute('update user set db_password=%s where user_id=%s;', [ss,person['user_id']])
                    mysql.connection.commit()   
                    flash("Password Updated Successfully !", "success")        
                    return redirect(url_for('student_profile'))
                except Exception as Ex:
                    print("Error creating MySQL User: %s"%(Ex))
                    flash("Password Not Updated !", "warning")        
                    return redirect(url_for('student_profile'))
                

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user where user_id = %s',[person['user_id']])
        student = cursor.fetchone()
        return render_template("Student/student_profile.html", user=person , password=student['db_password'])

    else:
        return redirect(url_for('login'))

@app.route("/student_database")
def student_database():
    if not session.get("id") is None and person["user"] == 'student':
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM database_users where user_id = %s',[person['user_id']])
        account = cursor.fetchall()
        return render_template("Student/student_database.html",value=account,user=person)

    else:
        return redirect(url_for('login'))

    
@app.route("/db_register", methods=["POST", "GET"])
def registers():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur = conn.cursor()   

    if request.method == "POST":

        result = request.form   
        software = result["database"]
        start_date = result["startdate"]
        end_date = result["enddate"]
        
        dbname = result["dbname"]
        remark = result["remark"]

        status = "Not Approved"


        
        cursor.execute('insert into database_users(user_id, db_software, start_date, end_date, db_name, Request_status, user_remark) values(%s,%s,%s,%s,%s,%s,%s)', [
                       person['user_id'],software,start_date,end_date, dbname, status, remark])
        mysql.connection.commit()
        return redirect(url_for('student_database'))
    
    #poste

    cur.execute('SELECT usename FROM pg_catalog.pg_user')
    datas = list(cur.fetchall())
    
    rowarray_lists = []
    for row in datas:
        ts = (row[0])
        rowarray_lists.append(ts)
    print(rowarray_lists)

    # sql 
    cursor.execute('SELECT User FROM mysql.user')
    rows = cursor.fetchall()
    rowarray_list = []
    for row in rows:
        t = (row['User'])
        rowarray_list.append(t)

    print(rowarray_list)
    return render_template("Student/student_db_register.html",user=person,list=json.dumps(rowarray_list),lists=json.dumps(rowarray_lists))



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

@app.route("/console")
def console():
    if not session.get("id") is None and person["user"] == 'student':

        rollno=person['rollno']
        message = rollno
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')

        print(base64_message)
        link="http://localhost:8888/?hostname=10.30.0.11&username="+rollno+"&password="+base64_message
        return webbrowser.open_new_tab(link)
        return redirect(url_for('home'))

    else:
        return redirect(url_for('login'))