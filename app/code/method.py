from app import *


@app.route("/")
def login():
    #return render_template("Student/student_home.html")
    if(not session.get("id") is None):
        if(person["user_type"] == 'student'):
            return redirect(url_for('home'))
        elif(person["user_type"] == 'provider'):
            return redirect(url_for('provider_home'))
        else:
            session.pop("id", None)
            return redirect(url_for('login'))
    else:
        return render_template("login.html")


