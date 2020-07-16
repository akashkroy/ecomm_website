import os
from flask import Flask
from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from datetime import datetime
from models import Users

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config["IMAGE_UPLOADS"] = "/mnt/d/Python_Learn/Magazine_website/static/images"
app.config["ALLOWED_IMAGE_EXTENTIONS"] = ["JPEG", "JPG", "PNG"]
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:toor@localhost:3306/ecomm"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def allowed_image(filename):
    #we want files that has a . in filename 
    if not "." in filename:
        return False
    
    # Split the extention from the filename
    ext = filename.rsplit(".",1)[1]
    
    # check if the extention is in ALLOWED_IMAGE_EXTENTIONS
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENTIONS"]:
        return True
    else:
        return False 


@app.route("/", methods=["GET", "POST"])
def dashboard():
    if request.form:
        products = (
            request.form["name"],
            request.form["product image"],
            request.form["description"],
            request.form["price"],
            request.form["quantity"],
            request.form["tag"]
        )
        print(products)
        if request.files:
            image = request.files["product image"]
            
            if image.filename == "":
                print("No Filename")
                return redirect(request.url)
            
            if allowed_image(image.filename):
                image.save(os.join(app.config["IMAGE_UPLOADS"], image.filename))
                print("Image Saved")
                return redirect(request.url)
    return render_template("dashboard.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email_id = request.form["email"]
        passphrase = request.form["password"]
        exists = Users.query.filter_by(user_email=email_id).first()
        if exists != None:
            duplicate =  '<span>An account with this username already exists</span>'
            return duplicate
        query = Users(first_name=firstname,last_name=lastname, user_email=email_id, password=passphrase, created_on=datetime.now())
        db.session.add(query)
        db.session.commit()
        return redirect(url_for("signup"))
    return render_template("signup.html")

class login_form(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email(message='Enter a valid Email')])
    passwd = StringField('password', validators=[DataRequired()])  
    submit = SubmitField('Log In')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = login_form(request.method)
    if request.method == "POST":
        form.email = request.form["email"]
        password = request.form["password"]
        
    return render_template("login.html")
if __name__=="__main__":
    app.run(debug=True)