from flask import Flask,render_template, url_for,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
import datetime

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

app = Flask(__name__)
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
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

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
    return render_template("contact.html")

@app.route("/post")
def post():
    return render_template("post.html")

if __name__=="__main__":
    app.run(debug=True)