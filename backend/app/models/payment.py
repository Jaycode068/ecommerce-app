class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    order = db.relationship('Order', back_populates='payment')

    def _init_(self, order, amount):
        self.order = order
        self.amount = amount

    def _repr_(self):
        return f"<Payment - Order ID: {self.order.id}, Amount: {self.amount}>"