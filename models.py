from flask import Flask
#from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sensitive import username,password

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:toor@localhost:3306/ecomm"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#metadata = MetaData(naming_convention=None)
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(64), nullable=False)
    last_name = db.Column('last_name', db.String(64), nullable=False)
    user_email = db.Column('user_email', db.String(100), unique=True, nullable=False)
    password = db.Column('password', db.String(160), nullable=False)
    role = db.Column('role', db.String(64), default='customer', nullable=False)
    created_on = db.Column('created_on', db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'User {self.user_email}'
    
class Address(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    street = db.Column('street', db.Text, nullable=False)
    city = db.Column('city', db.String(64), nullable=False)
    state = db.Column('state', db.String(64), nullable=False)
    zip = db.Column('zip_code', db.Integer, nullable=False)
    
    def __repr__(self):
        return f'Street {self.street}'                 

class Products(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(200), nullable=False)
    image = db.Column('image', db.String(100),nullable=False)
    description = db.Column('description', db.Text, nullable=True)
    price = db.Column('price', db.Float(), nullable = False)
    quantity = db.Column('quantity', db.Integer, nullable = False)
    category = db.Column('tags', db.Text(),nullable = True)
    created_on = db.Column('created_on', db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'Name {self.name}'

class Cart(db.Model):
    id = db.Column('id',db.Integer,primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'id {self.id}'

class Cart_Products(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    cart_id = db.Column('cart_id', db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column('product_id', db.Integer, db.ForeignKey('products.id'), nullable = False)
    quantity = db.Column('quantity', db.Integer, default=1)
    
    def __repr__(self):
        return f'id {self.id}'


class Payment(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    cc = db.Column('cc', db.Integer, nullable=False)
    expiry_month = db.Column('expiry_month', db.DateTime, nullable=False)
    cvv = db.Column('cvv', db.Integer, nullable=False)
    
    def __repr__(self):
        return f'Payment id {self.id}'
    

class Orders(db.Model):
    order_number = db.Column('order_number', db.Integer, primary_key=True)
    cart_id = db.Column('cart_id', db.Integer, db.ForeignKey('cart.id'), nullable=False)
    payment_id = db.Column('payment_id', db.Integer, db.ForeignKey('payment.id'), nullable=False)
    address_id = db.Column('address_id', db.Integer, db.ForeignKey('address.id'), nullable=False)
    status = db.Column('status', db.String(20), nullable=False)
    created_on = db.Column('created_on', db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'Order Number {self.order_number}'
db.create_all()