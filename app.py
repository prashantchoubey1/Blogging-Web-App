from flask import Flask,render_template, url_for,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
import datetime
from flask_mail import Mail, Message


try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

import json
 
# Opening JSON file
f = open('/Users/prashantchoubey/Documents/VS Workspace/Flask-Harry/Blogging-Web-App/templates/config.json')
params = json.load(f)['params']

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'prashantchoubey1995@gmail.com'
app.config['MAIL_PASSWORD'] = 'V3Siird2vxK44P'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# app.config['MAIL_SERVER']= params['MAIL_SERVER']
# app.config['MAIL_PORT'] = params['MAIL_PORT']
# app.config['MAIL_USERNAME'] = params['MAIL_USERNAME']
# app.config['MAIL_PASSWORD'] = params['MAIL_PASSWORD']
# app.config['MAIL_USE_TLS'] = params['MAIL_USE_TLS']
# app.config['MAIL_USE_SSL'] = params['MAIL_USE_SSL']
mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/UnknownBlogger'
db = SQLAlchemy(app)


class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(10), nullable=False)
    mes = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(12), nullable=True)



@app.route("/")
def home():
    return render_template("index.html",params=params)

@app.route("/about")
def about():
    return render_template("about.html",params=params)

@app.route("/contact", methods=["GET","POST"])
def contact():
    if(request.method == 'POST'):
        name = request.form.get("name")
        email = request.form.get("email")
        phone_num = request.form.get("phone_num")
        mes = request.form.get("message")
        date = datetime.datetime.now(pytz.timezone('Asia/Kolkata')) 
        contact = Contact(name=name,email=email,phone_num=phone_num,mes=mes,date=date)
        db.session.add(contact)
        db.session.commit()
        msg = Message('Thank you for your enquiry', 
                        sender = "prashantchoubey1995@gmail.com", 
                        recipients = ["choubey.prashant16@gmail.com"])
        mail.send(msg)
    return render_template("contact.html",params=params)

@app.route("/post")
def post():
    return render_template("post.html",params=params)

if __name__=="__main__":
    app.run(debug=True)