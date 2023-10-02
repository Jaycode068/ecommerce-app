from app.extension import db 

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    product = db.relationship('Product')
    order = db.relationship('Order', back_populates='items')

    def _init_(self, order, product, quantity):
        self.order = order
        self.product = product
        self.quantity = quantity

    def _repr_(self):
        return f"<OrderItem - Order ID: {self.order.id}, Product: {self.product.name}, Quantity: {self.quantity}>"