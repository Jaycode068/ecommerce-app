from app.extension import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    products = db.relationship('Product', back_populates='category')

    def _init_(self, name):
        self.name = name

    def _repr_(self):
        return f"<Category {self.name}>"