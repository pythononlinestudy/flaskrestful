from App.ext import db


class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_name = db.Column(db.String(16))
    c_age = db.Column(db.Integer, default=1)
