from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)


class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(30), nullable=False)
    item_price = db.Column(db.Float, nullable=False)
    item_amount = db.Column(db.Integer, nullable=False)
    item_exp_date = db.Column(db.String(30), nullable=False)