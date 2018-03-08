from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    notes = db.Column(db.String(120))

    def __init__(self, username, email, phone_number, notes):
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.notes = notes

    def __repr__(self):
        return "<Username %r>" % self.username

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    phone_number = fields.Str()
    email = fields.Str()
    notes = fields.Str()