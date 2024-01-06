from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin


db = SQLAlchemy()


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
    


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255), nullable=False)
    lname= db.Column(db.String(255),  nullable=False)
    mobile =db.Column(db.Integer)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    active = db.Column(db.Boolean())
    authenticated = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='roles_users',
                         backref=db.backref('users', lazy='dynamic'))
    
    @property
    def is_authorised(self):
        return self.authenticated
    
    @property
    def get_roles(self):
        return [role.name for role in self.roles]
    
    

    def __repr__(self):
        return '<User %r>' % self.email
    
class Profile(db.Model):
    __tablename__ = 'profile'

    id=db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    quantity = db.Column(db.Integer)
    date_purchased=db.Column(db.String)
    def __repr__(self):
        return  str(self.product_id)+" "+str(self.quantity)

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.JSON, unique=True)
    products = db.relationship("Product")
    is_approved= db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Category %r>' % self.name

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String)
    manufacture_date = db.Column(db.String)
    expiry_date = db.Column(db.String)
    rate_per_unit = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    quantity= db.Column(db.Integer)
    profile = db.relationship("Profile")
    def __repr__(self):
        return '<Product %r>' % self.name

class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer)
    cart_product= db.relationship("Product")
    def __repr__(self):
        # to return product name and quantity
        return  str(self.product_id)+" "+str(self.quantity)
        # return str(self.id) +" "+ str(self.user_id) +" "+ str(self.product_id)+" "+ str(self.quantity)
