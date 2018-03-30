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

VERSION = "v1"

# Error responses
def bad_request(message):
    response = jsonify({'error': message})
    response.status_code = 400
    return response

def not_found(message):
    response = jsonify({'error': message})
    response.status_code = 404
    return response

# Set "homepage" to index.html
@app.route("/")
def index():
    return render_template("index.html")

################################################################################
## Users CRUD Endpoints
################################################################################
@app.route("/api/{version}/users/".format(version=VERSION), methods=["POST"])
def add_user():
    body = request.get_json()
    email = body.get("email")
    username = body.get("username")

    if not body or not username or not email:
        return bad_request("Username and e-mail must be provided")

    if not User.query.filter_by(username=username).count():
        user = User(body)
        db.session.add(user)
        db.session.commit()
        user_added = UserSchema().dump(user)
        return jsonify(user_added.data), 201
    else:
        return bad_request("User already in database")

@app.route("/api/{version}/users/<int:id>".format(version=VERSION), methods=["PUT"])
def update_user(id):
    body = request.get_json()
    email = body.get("email")
    username = body.get("username")

    if not username or not email:
        return bad_request("Username and e-mail must be provided")

    if User.query.filter_by(username=username).count():
        return bad_request("Username already exists, select another username")
    try:
        user = User.query.get(id)
        user.email = email
        user.username = username

        user_updated = UserSchema().dump(user)
        db.session.commit()
        return jsonify(user_updated.data), 201
    except:
        return not_found("Could not find user with given ID")

@app.route("/api/{version}/users".format(version=VERSION), methods=["GET"])
def get_users():
    response = {
        "users": []
    }
    users = User.query.all()
    for user in users:
        user_obj = UserSchema().dump(user)
        response["users"].append(user_obj.data)
    return jsonify(response)

@app.route("/api/{version}/users/<int:id>/".format(version=VERSION), methods=["GET"])
def get_user(id):
    try:
        user = User.query.filter_by(user_id=id).first_or_404()
        user_result = UserSchema().dump(user)
        return jsonify(user_result.data)
    except:
        return not_found("Could not find user with given ID")

@app.route("/api/{version}/users/<int:id>".format(version=VERSION), methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if user:
        username = user.username
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Successfully deleted {user}".format(user=username)}), 200
    else:
        return bad_request("User does not exist")


################################################################################
## Therapists CRUD Endpoints
################################################################################
@app.route("/api/{version}/therapists/".format(version=VERSION), methods=["POST"])
def add_therapist():
    body = request.get_json()
    name = body.get("name")
    location = body.get("location")
    specialty = body.get("specialty")

    if not body or not name or not specialty or not location:
        return bad_request("Name, location, and specialty must be provided")

    if not Therapist.query.filter_by(name=name).count():
        therapist = Therapist(body)
        db.session.add(therapist)
        db.session.commit()
        therapist_added = TherapistSchema().dump(therapist)
        return jsonify(therapist_added.data), 201
    else:
        return bad_request("Therapist already in database")

@app.route("/api/{version}/therapists/<int:id>".format(version=VERSION), methods=["PUT"])
def update_therapist(id):
    body = request.get_json()
    name = body.get("name")
    location = body.get("location")
    specialty = body.get("specialty")

    if not name or not specialty or not location:
        return bad_request("Name, location, and specialty must be provided")

    if Therapist.query.filter_by(name=name).count():
        return bad_request("Therapist already exists, select another name")

    try:
        therapist = Therapist.query.get(id)
        therapist.name = name
        therapist.location = location
        therapist.specialty = specialty

        therapist_updated = TherapistSchema().dump(therapist)
        db.session.commit()
        return jsonify(therapist_updated.data), 201
    except:
        return not_found("Could not find therapist with given ID")

@app.route("/api/{version}/therapists/".format(version=VERSION), methods=["GET"])
def get_therapists():
    response = {
        "therapists": []
    }
    therapists = Therapist.query.all()
    for therapist in therapists:
        therapist_obj = TherapistSchema().dump(therapist)
        response["therapists"].append(therapist_obj.data)
    return jsonify(response)

@app.route("/api/{version}/therapists/<int:id>".format(version=VERSION), methods=["GET"])
def get_therapist(id):
    try:
        therapist = Therapist.query.filter_by(therapist_id=id).first_or_404()
        therapist_result = TherapistSchema().dump(therapist)
        return jsonify(therapist_result.data)
    except:
        return not_found("Could not find therapist with given ID")

@app.route("/api/{version}/therapists/<int:id>".format(version=VERSION), methods=["DELETE"])
def delete_therapist(id):
    therapist = Therapist.query.get(id)
    if therapist:
        name = therapist.name
        db.session.delete(therapist)
        db.session.commit()
        return jsonify({"message": "Successfully deleted {therapist}".format(therapist=name)}), 200
    else:
        return bad_request("Therapist does not exist")

if __name__ == "__main__":
    app.debug = True
    app.run()