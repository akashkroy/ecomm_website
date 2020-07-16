from flask import Flask
#from sqlalchemy import MetaData
import sqlalchemy


from models import Users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:toor@localhost:3306/ecomm"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
email = 'mail@akash.com'
passwd = 'grrrr'
exists = Users.query.filter_by(user_email=email).first()
#result = db.session.count(Users.user_email).where(Users.user_email==email)
check_email = Users.query.filter_by(user_email==email & password==passwd)
#check_password = Users.query.filter_by(password=password).first()

print(check_email)