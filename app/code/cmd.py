import pyrebase

firebaseConfig={
    "apiKey": "AIzaSyDCL31T4QStQlXNtxBF7GHpZqljSRh_h-M",
    "authDomain": "db-console.firebaseapp.com",
    "databaseURL": "https://db-console-default-rtdb.firebaseio.com",
    "projectId": "db-console",
    "storageBucket": "db-console.appspot.com",
    "messagingSenderId": "91281671272",
    "appId": "1:91281671272:web:f97ee0cd7f4ecc508ce7dd"
    }


firebase=pyrebase.initialize_app(firebaseConfig)

db=firebase.database()

#Push Data
data={"age":20, "address":["new york", "los angeles"]}
print(db.push(data)) #unique key is generated

#Create paths using child
#data={"name":"Jane", "age":20}
#db.child("Branch").child("Employees").push(data)

#Create your own key
data={"age":20, "address":["new york", "los angeles"]}
db.child("John").set(data)

#Create your own key + paths with child
data={"name":"John", "age":20, "address":["new york", "los angeles"]}
db.child("Branch").child("Employee").child("male employees").child("John's info").set(data)

