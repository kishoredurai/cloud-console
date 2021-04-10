from app import  *


@app.route("/provider/profile")
def profile():
    if not session.get("id") is None and person["user_type"] == 'provider':

       return render_template("provider/provider_profile.html", email=person["email"], name=person["name"],contact=person["contact"])

    else:
        return redirect(url_for('login'))



@app.route("/provider/home")
def provider_home():
    if not session.get("id") is None and person["user_type"] == 'provider':

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        account=cursor.execute('SELECT COUNT(*) FROM database_users')
        print(account)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sas=cursor.execute('SELECT COUNT(*) FROM database_users where db_status="Active"')
        print(sas)
        return render_template("provider/provider_home.html", email=person["email"], name=person["name"],data=account,ac=sas)

    else:
        return redirect(url_for('login'))




@app.route("/provider/database/update", methods=["POST", "GET"])
def provider_update():
    
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
            cursor.execute('insert into db_approval_status(db_id, admin_id, update_status, provider_remark) values(%s,%s,"Approved",%s)', [ss,id,remark])
            mysql.connection.commit()
            cursor.execute('update database_users set db_status = "Deactive" , Request_status = "Approved" where db_id=%s;', [ss])
            mysql.connection.commit()            
            return redirect(url_for('database'))
   


        

@app.route("/provider/database")
def database():
    if not session.get("id") is None and person["user_type"] == 'provider':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM database_users,user where database_users.user_id=user.user_id ORDER BY applied_date DESC')
        account = cursor.fetchall()
        return render_template("provider/provider_database.html", email=person["email"], name=person["name"], value=account)

    else:
        return redirect(url_for('login'))


