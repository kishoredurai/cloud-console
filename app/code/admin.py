from app import *


@app.route("/admin/home")
def admin_home():
    if not session.get("id") is None and person["user"] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        account=cursor.execute('SELECT COUNT(*) FROM database_users')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sas=cursor.execute('SELECT COUNT(*) FROM database_users where db_status="Active"')
        return render_template("admin/admin_home.html", email=person["email"], name=person["name"],data=account,ac=sas)

    else:
        return redirect(url_for('login'))

@app.route('/admin/test')
def main(): 
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result = cur.execute("SELECT * FROM `user`")
    employee = cur.fetchall()   
    return render_template('admin/admin_test.html', employee=employee)

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
        result = cur.execute("SELECT * FROM tbl_employee WHERE id = %s", [employee_id])
        rsemployee = cur.fetchall()
        employeearray = []
        for rs in rsemployee:
            employee_dict = {
                    'Id': rs['id'],
                    'emp_name': rs['name'],
                    'address': rs['address'],
                    'gender': rs['gender'],
                    'designation': rs['designation'],
                    'age': rs['age']}
            employeearray.append(employee_dict)
        return json.dumps(employeearray)