class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_price = db.Column(db.Float, nullable=False)
    items = db.relationship('OrderItem', back_populates='order')
    user = db.relationship('User', back_populates='orders')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def _init_(self, user, total_price):
        self.user = user
        self.total_price = total_price

    def _repr_(self):
        return f"<Order - User: {self.user.username}, Total Price: {self.total_price}>"