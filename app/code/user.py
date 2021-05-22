from app import  *

@app.route("/home")
def home():
    if not session.get("id") is None and person["user"] == 'student':

        return render_template("Student/student_home.html",user=person)

    else:
        return redirect(url_for('login'))


@app.route("/profile", methods=["POST", "GET"])
def student_profile():
    cur = conn.cursor()   
    if not session.get("id") is None and person["user"] == 'student':
               
        if request.method == "POST":
            if request.form.get("update"):
                result = request.form  # Get the data
                ss = result["sql_dbpasswd"]
                db_soft = result["db_software"]

                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

                if(db_soft == 'SQL'):
                    try:
                        sqlCreateUser = "ALTER USER '%s'@'localhost' IDENTIFIED BY '%s';"%(person['rollno'],ss)
                        cursor.execute(sqlCreateUser)
                        cursor.execute('update db_login_user set db_password=%s where db_software = %s and user_id=%s;', [ss,db_soft,person['user_id']])
                        mysql.connection.commit()   
                        flash("Password Updated Successfully !", "success")        
                        return redirect(url_for('student_profile'))
                    except Exception as Ex:
                        print("Error creating MySQL User: %s"%(Ex))
                        flash("Password Not Updated !", "warning")        
                        return redirect(url_for('student_profile'))


            if request.form.get("update_post"):
                result = request.form  # Get the data
                ss = result["dbpasswd"]
                db_soft = result["db_software"]

                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

                if(db_soft == 'PostgreSQL'):
                    print('post')
                    try:
                        query = "ALTER USER "'"'+person['rollno']+'"'" WITH PASSWORD '"+ss+"' ;"
                        cur.execute(sql.SQL(query).format())
                        cursor.execute('update db_login_user set db_password=%s where db_software = %s and user_id=%s;', [ss,db_soft,person['user_id']])
                        mysql.connection.commit()   

                        print('enetered')

                        flash(" postegs Password Updated Successfully !", "success")        
                        return redirect(url_for('student_profile'))
                    except Exception as Ex:
                        print("Error creating MySQL User: %s"%(Ex))
                        flash("Password Not Updated !", "warning")        
                        return redirect(url_for('student_profile'))

                
                    

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)


        sql_db='Deactive'
        pos_db='Deactive'
        cursor.execute('SELECT * FROM db_login_user where user_id = %s',[person['user_id']])
        db = cursor.fetchall()
        for row in db:
            if(row['db_software']=='SQL' and row['db_user_status'] == 'Active'):
                sql_db=row['db_password']
            if(row['db_software']=='PostgreSQL' and row['db_user_status'] == 'Active'):
                pos_db=row['db_password']
        return render_template("Student/student_profile.html", user=person , sql_db = sql_db ,pos_db=pos_db)

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

    cur.execute('SELECT datname FROM pg_database;')
    datas = list(cur.fetchall())
    
    rowarray_lists = []
    for row in datas:
        ts = (row[0])
        rowarray_lists.append(ts)
    print(rowarray_lists)

    # sql 
    cursor.execute('show DATABASES')
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