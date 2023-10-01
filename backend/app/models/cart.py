class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', back_populates='cart')
    product = db.relationship('Product')

    def _init_(self, user, product, quantity):
        self.user = user
        self.product = product
        self.quantity = quantity

    def _repr_(self):
        return f"<Cart Item - User: {self.user.username}, Product: {self.product.name}, Quantity: {self.quantity}>"