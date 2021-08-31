from app import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), index=True, unique=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(64), nullable=False)
    ads = db.relationship('Ads', backref='owner')


class Ads(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), index=True, unique=True)
    description = db.Column(db.String(255))
    adv_date = db.Column(db.DateTime)
