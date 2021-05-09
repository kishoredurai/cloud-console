from app import  *


@app.route("/provider/profile")
def profile():
    if not session.get("id") is None and person["user"] == 'provider':
        return render_template("provider/provider_profile.html", email=person["email"], name=person["name"])

    else:
        return redirect(url_for('login'))


@app.route("/provider/home")
def provider_home():
    if not session.get("id") is None and person["user"] == 'provider':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        account=cursor.execute('SELECT COUNT(*) FROM database_users')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sas=cursor.execute('SELECT COUNT(*) FROM database_users where db_status="Active"')
        return render_template("provider/provider_home.html", email=person["email"], name=person["name"],data=account,ac=sas)

    else:
        return redirect(url_for('login'))



@app.route("/provider/database/details", methods=["POST", "GET"])
def provider_database_details():
    if not session.get("id") is None and person["user"] == 'provider':
                
        if request.method == "POST":
            if request.form.get("submit_a"):
                result = request.form  # Get the data
                ss = result["submit_a"]
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM database_users,user where database_users.user_id=user.user_id and database_users.db_id=%s',[ss])
                data = cursor.fetchone()  
                return render_template("provider/provider_db_approve.html",email=person["email"], name=person["name"],data=data)


            if request.form.get("approve"):
                result = request.form  # Get the data
                ss = result["approve"]
                id=session.get("id")
                remark = result["provider_remark"]
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM database_users where db_id=%s',[ss])
                data = cursor.fetchone() 
                if(data['db_software']=='SQL'):
                    SQL_db_create_check(ss)
                elif(data['db_software']=='PostgreSQL'):
                    postgre_db_create_check(ss)

                cursor.execute('insert into db_approval_status(db_id, admin_id, update_status, provider_remark) values(%s,%s,"Approved",%s)', [ss,id,remark])
                mysql.connection.commit()
                return redirect(url_for('database'))
    
            if request.form.get("reject"):
                result = request.form  # Get the data
                ss = result["reject"]
                id=session.get("id")
                remark = result["provider_remark"]
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('insert into db_approval_status(db_id, admin_id, update_status, provider_remark) values(%s,%s,"Rejected",%s)', [ss,id,remark])
                mysql.connection.commit()
                cursor.execute('update database_users set db_status = "Deactive" , Request_status = "Rejected" where db_id=%s;', [ss])
                mysql.connection.commit()            
                return redirect(url_for('database'))


        

@app.route("/provider/database")
def database():
    if not session.get("id") is None and person["user"] == 'provider':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM database_users,user where database_users.user_id=user.user_id ORDER BY applied_date DESC')
        account = cursor.fetchall()
        return render_template("provider/provider_database.html", email=person["email"], name=person["name"], value=account)

    else:
        return redirect(url_for('login'))


@app.route("/provider/student_details")
def provider_student_details():
    if not session.get("id") is None and person["user"] == 'provider':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user ')
        account = cursor.fetchall()
        return render_template("provider/provider_student.html", email=person["email"], name=person["name"], value=account)

    else:
        return redirect(url_for('login'))


   















def SQL_db_create_check(db_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)    
    cursor.execute('SELECT * FROM database_users,user where database_users.user_id=user.user_id and database_users.db_id=%s',[db_id])
    data = cursor.fetchone() 
    cursor.execute('SELECT * FROM mysql.user where user=%s',[data['rollno']])
    datas = cursor.fetchall()
    if not datas:
        try:
            sqlCreateUser = "CREATE USER '%s'@'localhost' IDENTIFIED BY '%s';"%(data['rollno'],data['db_password'])
            cursor.execute(sqlCreateUser)
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
            query = "CREATE USER "'"'+data['rollno']+'"'" LOGIN PASSWORD '"+data['db_password']+"';"
            cur.execute(sql.SQL(query).format())
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
    try:
        sqlCreateUser = "GRANT ALL PRIVILEGES ON %s.* TO '%s'@'localhost' IDENTIFIED BY '%s';"%(data['db_name'],data['rollno'],data['db_password'])
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