from app import  *


@app.route("/provider/profile")
def profile():
    if not session.get("USERNAME") is None and session["user_type"]=='provider':

       return render_template("provider/provider_profile.html", email=person["email"], name=person["name"],contact=person["contact"])

    else:
        return redirect(url_for('login'))




@app.route("/provider/home")
def provider_home():
    if not session.get("USERNAME") is None and session["user_type"]=='provider':

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

        

@app.route("/provider/database")
def database():
    if not session.get("USERNAME") is None and session["user_type"]=='provider':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM database_users,user where database_users.user_id = user.user_id')
        account = cursor.fetchall()
        return render_template("provider/provider_database.html", email=person["email"], name=person["name"], value=account)

    else:
        return redirect(url_for('login'))


