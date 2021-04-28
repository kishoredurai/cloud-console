from flask import Flask
from flask_mail import Mail, Message

app = Flask(_name_)
mail = Mail(app)  # instantiate the mail class

# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cloud@bitsathy.ac.in'
app.config['MAIL_PASSWORD'] = 'Cloud@987'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

msg = Message('Hello',sender='cloud@bitsathy.ac.in',recipients=['kishore.ct19@bitsathy.ac.in'])
msg.body = 'Hello Flask message sent from Flask-Mail'
mail.send(msg)


if __name__ == '__main__':
   app.run(debug = True)