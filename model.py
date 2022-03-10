from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ProductModel(db.Model):
    __tablename__ = 'product'

    product_id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR, nullable=False)
    price = db.Column(db.INTEGER, nullable=False)
    description = db.Column(db.VARCHAR, nullable=False)
    quantity = db.Column(db.INTEGER, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, price, description, quantity, created_date):
        # self.product_id = product_id
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity
        self.created_date = created_date

    def __repr__(self):
        return f"<Product {self.name}>"