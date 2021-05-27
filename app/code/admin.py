from app import *


@app.route("/admin/home")
def admin_home():
    if not session.get("id") is None and person["user"] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        return render_template("admin/admin_home.html", email=person["email"], name=person["name"])
    else:
        return redirect(url_for('login'))

@app.route('/admin/user')
def main(): 
    if not session.get("id") is None and person["user"] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM `user`")
        employee = cursor.fetchall()   
        return render_template('admin/admin_user.html', employee=employee)
    else:
        return redirect(url_for('login'))

@app.route('/insert', methods=['GET', 'POST'])
def insert():   
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST': 
        name = request.form['name']
        address = request.form['address']
        gender = request.form['gender']
        designation = request.form['designation']
        age = request.form['age']
        cur.execute("INSERT INTO tbl_employee (name, address, gender, designation, age) VALUES (%s, %s, %s, %s, %s)",[name, address, gender, designation, age])
        mysql.connection.commit()
        cur.close()
    return jsonify('success')
 
@app.route('/select', methods=['GET', 'POST'])
def select():   
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST': 
        employee_id = request.form['employee_id']
        print(employee_id)      
        result = cur.execute("SELECT * FROM user WHERE user_id = %s", [employee_id])
        rsemployee = cur.fetchall()
        employeearray = []
        for rs in rsemployee:
            employee_dict = {
                    'Id': rs['user_id'],
                    'name': rs['name'],
                    'rollno': rs['rollno'],
                    'department': rs['department'],
                    'emailid': rs['email_id'],
                    'mobile': rs['mobile'],
                    'user_type': rs['user_type'],
                    'account_status': rs['account_status']}
            employeearray.append(employee_dict)
        return json.dumps(employeearray)


@app.route('/user/update', methods=['GET', 'POST'])
def admin_user_update():   
    
    if not session.get("id") is None and person["user"] == 'admin':

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            if request.form.get("block"):
                result = request.form  # Get the data
                user_id = result["block"]
                cur.execute("update user set account_status='no' where user_id=%s",[user_id])
                mysql.connection.commit()
                return redirect(url_for('main'))


            if request.form.get("unblock"):
                result = request.form  # Get the data
                user_id = result["unblock"]
                cur.execute("update user set account_status='yes' where user_id=%s",[user_id])
                mysql.connection.commit()
                return redirect(url_for('main'))
