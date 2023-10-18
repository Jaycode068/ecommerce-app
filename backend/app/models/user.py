from datetime import datetime
from app.extension import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    
    confirmpasswd = ''
    addresses = db.relationship('Address', back_populates='user', cascade='all, delete-orphan')
    orders = db.relationship('Order', back_populates='user', cascade='all, delete-orphan')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    
    def _init_(self, username, email):
        self.username = username
        self.email = email

    def _repr_(self):
        return f"<User {self.username}>"