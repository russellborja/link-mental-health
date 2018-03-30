from flask import Flask, render_template, request, jsonify
from flask_heroku import Heroku
from db.models import db, User, UserSchema, Therapist, TherapistSchema
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/russellborja"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db.init_app(app)
heroku = Heroku(app)

class Error(Exception):
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = "ERROR: %s" % self.message
        return rv

@app.errorhandler(Error)
def handle_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

# Set "homepage" to index.html
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/v1/users/", methods=["POST"])
def add_user():
    body = request.get_json()

    email = body.get("email")
    username = body.get("username")

    if not username or not email:
        raise Error("Username and e-mail must be provided", 400)

    if not User.query.filter_by(username=username).count():
        user = User(body)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            raise Error(e, 400)
        return jsonify({"message": "Succesfully added user."}), 201
    else:
        raise Error("User already in database", 400)

@app.route("/api/v1/users/<int:id>", methods=["PUT"])
def update_user(id):
    body = request.get_json()

    email = body.get("email")
    username = body.get("username")

    if not username or not email:
        raise Error("Username and e-mail must be provided", 400)
    try:
        user = User.query.get(id)
        user.email = email
        user.username = username
    except Exception as e:
        raise Error("Could not find therapist with given ID", 404)

    try:
        db.session.commit()
    except Exception as e:
        raise Error(e, 400)
    return jsonify(user), 201

@app.route("/api/v1/users/<int:id>/", methods=["GET"])
def get_user(id):
    try:
        user = User.query.filter_by(user_id=id).one()
    except Exception as e:
        raise Error("Could not find user with given ID", 404)
    user_result = UserSchema().dump(user)

    if user_result.errors:
        raise Error("Encountered errors retrieving user", 500, user_result.errors)
    return jsonify(user_result.data), 200

@app.route("/api/v1/therapists/", methods=["POST"])
def add_therapist():
    body = request.get_json()

    name = body.get("name")
    location = body.get("location")
    specialty = body.get("specialty")

    if not name or not specialty or not location:
        raise Error("Name, location, and specialty must be provided", 400)

    if not Therapist.query.filter_by(name=name).count():
        therapist = Therapist(body)
        try:
            db.session.add(therapist)
            db.session.commit()
        except Exception as e:
            raise Error(e, 400)
        return jsonify(therapist), 201
    else:
        raise Error("Therapist already in database", 400)

@app.route("/api/v1/therapists/<int:id>", methods=["PUT"])
def update_therapist(id):
    body = request.get_json()

    name = body.get("name")
    location = body.get("location")
    specialty = body.get("specialty")

    if not name or not specialty or not location:
        raise Error("Name, location, and specialty must be provided", 400)
    try:
        therapist = Therapist.query.get(id)
        therapist.name = name
        therapist.location = location
        therapist.specialty = specialty
    except Exception as e:
        raise Error("Could not find therapist with given ID", 404)

    try:
        db.session.commit()
    except Exception as e:
        raise Error(e, 400)
    return jsonify(therapist), 201

@app.route("/api/v1/therapists/<int:id>", methods=["GET"])
def get_therapist(id):
    try:
        therapist = Therapist.query.filter_by(therapist_id=id).one()
    except Exception as e:
        raise Error("Could not find therapist with given ID", 404)
    therapist_result = TherapistSchema().dump(therapist)

    if therapist_result.errors:
        raise Error("Encountered errors retrieving user", 500, therapist_result.errors)
    return jsonify(therapist_result.data), 200
    

if __name__ == "__main__":
    app.debug = True
    app.run()