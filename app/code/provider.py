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


   














