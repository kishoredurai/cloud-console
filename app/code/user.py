from app import  *

@app.route("/home")
def home():
    if not session.get("id") is None and person["user_type"] == 'student':

        return render_template("Student/student_home.html",user=person)

    else:
        return redirect(url_for('login'))


@app.route("/profile", methods=["POST", "GET"])
def student_profile():
    if not session.get("id") is None and person["user_type"] == 'student':
               
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
    if not session.get("id") is None and person["user_type"] == 'student':
        
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
