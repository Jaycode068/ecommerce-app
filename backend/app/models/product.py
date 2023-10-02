from app.extension import db 

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='products')

    def _init_(self, name, price, description, category):
        self.name = name
        self.price = price
        self.description = description
        self.category = category

    def _repr_(self):
        return f"<Product {self.name}>"