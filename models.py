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
    authenticated = db.Column(db.Integer())
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
    
