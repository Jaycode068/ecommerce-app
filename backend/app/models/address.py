from app.extension import db

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    user = db.relationship('User', back_populates='address')

    def _init_(self, user, street, city, state, postal_code):
        self.user = user
        self.street = street
        self.city = city
        self.state = state
        self.postal_code = postal_code

    def _repr_(self):
        return f"<Address - User: {self.user.username}, Street: {self.street}, City: {self.city}>"