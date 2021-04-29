from app import  *



   



# Sign up/ Register





@app.route("/signup")
def signup():
    return render_template("signup.html")



# Welcome page









# If someone clicks on register, they are redirected to /register


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":  # Only listen to POST
        result = request.form  # Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        contact = result["cont"]
        try:
            # Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            # Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            # Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            print(email, password,contact)
            # Append data to the firebase realtime database
            data = {"name": name, "email": email, "contact": contact}
            db.child("users").child(person["uid"]).set(data)
            # Go to welcome page
            return redirect(url_for('welcome'))
        except:
            # If there is any error, redirect to register
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))

    # return Response("<h1>Success!</h1>")




###### Student Login  #########



