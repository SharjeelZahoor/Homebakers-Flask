from homebaker import db
from datetime import datetime,date
from flask_login import UserMixin
# Cake Model FK table
class Cakes(db.Model):
        id=db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(50),nullable=False)
        ctype = db.Column(db.String(50),nullable=False)
        csize = db.Column(db.String(50),nullable=False)
        cflavor = db.Column(db.String(50),nullable=False)
        details = db.Column(db.Text,nullable=True)
        price = db.Column(db.Float,nullable=False, default=0.0)
        photo = db.Column(db.String(255),nullable=True, default='no-image.png')
        status = db.Column(db.String(20),nullable=True, default='Active')
        date_created = db.Column(db.DateTime, default=datetime.utcnow)

        # flavor_id = db.Column(db.Integer, db.ForeignKey('flavors.id'))
        cart=db.relationship('Carts',backref=db.backref('cakecart')) # PK -> FK (cart)
        item=db.relationship('Items',backref=db.backref('cakeitem')) # PK -> FK (Item)
        def __repr__(self):
                return self.title  
 # Cake flavor Model PK table
class Flavors(db.Model):
        id=db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(50),nullable=False)
        date_created = db.Column(db.DateTime, default=datetime.utcnow)

        # Cake= failed to locate class, Cakes =  relationship 'cakes' expects a class or a mapper argument (received: <class 'sqlalchemy.sql.schema.Table'>)
        # cakes=db.relationship('Cakes',backref=db.backref('flavorof')) #primaryjoin="Flavors.id == Cakes.flavor_id"
        def __repr__(self):
                return self.title       

class Types(db.Model):
        id=db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(50),nullable=False)
        date_created = db.Column(db.DateTime, default=datetime.utcnow)
        # cakes=db.relationship('Types',backref='types',primaryjoin="Types.id==Cakes.type_id")
        def __repr__(self):
                return self.title       
 # Cake Size Model
class Sizes(db.Model):
        id=db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(50),nullable=False)
        date_created = db.Column(db.DateTime, default=datetime.utcnow)
        # cakes=db.relationship('Sizes',backref='sizes',uselist=True,lazy=True,primaryjoin="Sizes.id == Cakes.size_id")
        def __repr__(self):
                return self.title       
# User Model
class Users(db.Model,UserMixin):
        id=db.Column(db.Integer, primary_key=True)
        loginid = db.Column(db.String(200),unique=True,nullable=False)
        password = db.Column(db.String(255),nullable=False)
        name = db.Column(db.String(100),nullable=False)
        contact = db.Column(db.String(20),nullable=False)
        email = db.Column(db.String(200),nullable=False)
        address = db.Column(db.String(255),nullable=True)
        utype = db.Column(db.String(15),nullable=True, default='Customer')
        status = db.Column(db.String(15),nullable=True, default='Active')
        photo = db.Column(db.String(100),nullable=True, default='user.png')
        date_created = db.Column(db.DateTime, default=datetime.utcnow)
        cart=db.relationship('Carts',backref=db.backref('usercart')) # PK -> FK (Cart)
        order=db.relationship('Orders',backref=db.backref('userorder')) # PK -> FK (Order)
        item=db.relationship('Items',backref=db.backref('useritem')) # PK -> FK (Item)
        def __repr__(self):
                return f'{self.name} : {self.loginid}'
# FK
class Carts(db.Model):
        id=db.Column(db.Integer, primary_key=True)
        product_id=db.Column(db.Integer, db.ForeignKey('cakes.id')) # FK -> PK (Cake)
        customer_id=db.Column(db.Integer, db.ForeignKey('users.id')) # FK -> PK (User)
        qty=db.Column(db.Integer, default=1,nullable=True)
        customization=db.Column(db.String(10),nullable=True, default='No')
        ctext = db.Column(db.String(255),nullable=True)
        cprice=db.Column(db.Float,nullable=False, default=0.0)
        status=db.Column(db.String(50),nullable=True, default='Pending') # pending, requested, approved
        date_created = db.Column(db.DateTime, default=datetime.utcnow)
        def __repr__(self):
                return f' : {self.qty}'

class Orders(db.Model):
        id=db.Column(db.Integer, primary_key=True)
        customer_id=db.Column(db.Integer, db.ForeignKey('users.id')) # FK -> PK (User)
        date=db.Column(db.Date, default=date.today)
        price=db.Column(db.Float,nullable=False, default=0.0)
        shippment=db.Column(db.Float,nullable=False, default=100.0)
        pmethod=db.Column(db.String(50),nullable=True, default='COD')
        address=db.Column(db.String(255),nullable=True)
        status=db.Column(db.String(50),nullable=True, default='Pending')
        date_created = db.Column(db.DateTime, default=datetime.utcnow)
        item=db.relationship('Items',backref=db.backref('orderitem')) # PK -> FK (Item)
        def __repr__(self):
                return f'{self.price} : {self.date}'

class Items(db.Model):
        id=db.Column(db.Integer, primary_key=True)
        product_id=db.Column(db.Integer, db.ForeignKey('cakes.id')) # FK -> PK (Cake)
        customer_id=db.Column(db.Integer, db.ForeignKey('users.id')) # FK -> PK (User)
        order_id=db.Column(db.Integer, db.ForeignKey('orders.id')) # FK -> PK (Order)
        price=db.Column(db.Float,nullable=False, default=0.0)
        qty=db.Column(db.Integer, default=1,nullable=True)
        customization=db.Column(db.String(10),nullable=True, default='No')
        ctext = db.Column(db.String(255),nullable=True)
        cprice=db.Column(db.Float,nullable=False, default=0.0)
        date_created = db.Column(db.DateTime, default=datetime.utcnow)
        def __repr__(self):
                return f'{self.qty} : {self.price}'

class Customer(db.Model,UserMixin):
        id=db.Column(db.Integer, primary_key=True)
        loginid = db.Column(db.String(200),unique=True,nullable=False)
        