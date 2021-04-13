from app import *

def db_create_check(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM database_users,user where database_users.user_id=user.user_id and database_users.db_id=%s',[id])
    data = cursor.fetchone() 
    cursor.execute('create database %s', [data["db_name"]])
    mysql.connection.commit()  
    today = date.today()
    if(data["start_date"] <= today):
        print("created")
        cursor.execute('update database_users set db_status = "Active" , Request_status = "Approved" where db_id=%s;', [id])
        mysql.connection.commit()  
    else:
        print("not created")  
        cursor.execute('update database_users set db_status = "Deactive" , Request_status = "Approved" where db_id=%s;', [id])
        mysql.connection.commit() 
    



