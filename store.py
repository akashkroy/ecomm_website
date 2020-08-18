import os
from flask import Flask
from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
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
    form = SignupForm(request.method)
    if form.validate_on_submit():
        existing_user = Users.query.filter_by(user_email=form.email.data).first()
        if existing_user == None:
            query = Users(first_name=form.firstname.data,last_name=form.lastname.data, user_email=form.email.data, password=form.password.data, created_on=datetime.now())
            db.session.add(query)
            db.session.commit()
            return redirect("/")
        flash('A user already exists with this email.')
    return render_template("signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = login_form(request.method)
    if request.method == "POST":
        form.email = request.form["email"]
        form.password = request.form["password"]
        
    return render_template("login.html", form=form)
if __name__=="__main__":
    app.run(debug=True)