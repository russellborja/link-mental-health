from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    notes = db.Column(db.String(120))

    def __init__(self, data):
        self.username = data.get("username")
        self.email = data.get("email")
        self.phone_number = data.get("phone_number")
        self.notes = data.get("notes")

    def __repr__(self):
        return "<Username %r>" % self.username

class Therapist(db.Model):
    __tablename__ = "therapists"
    therapist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    location = db.Column(db.String(120))
    specialty = db.Column(db.String(120))
    treatment_type = db.Column(db.String(120))
    bio = db.Column(db.String(120))
    average_wait_time = db.Column(db.Integer)
    summary = db.Column(db.String(200))

    def __init__(self, data):
        self.name = data.get("name")
        self.location = data.get("location")
        self.specialty = data.get("specialty")
        self.treatment_type = data.get("treatment_type")
        self.bio = data.get("bio")
        self.average_wait_time = data.get("average_wait_time")
        self.summary = data.get("summary")

    def __repr__(self):
        return "<Therapist %r>" % self.name

class UserSchema(Schema):
    user_id = fields.Int()
    username = fields.Str()
    phone_number = fields.Str()
    email = fields.Str()
    notes = fields.Str()

class TherapistSchema(Schema):
    therapist_id = fields.Int()
    name = fields.Str()
    location = fields.Str()
    specialty = fields.Str()
    treatment_type = fields.Str()
    bio = fields.Str()
    average_wait_time = fields.Int()
    summary = fields.Str()
