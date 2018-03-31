from flask import Flask, render_template
from flask_heroku import Heroku
from db.models import db
from routes import therapists, users
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/russellborja"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db.init_app(app)
heroku = Heroku(app)

VERSION = "v1"

# Set "homepage" to index.html
@app.route("/")
def index():
    return render_template("index.html")


################################################################################
## Users CRUD Endpoints
################################################################################
@app.route("/api/{version}/users/".format(version=VERSION), methods=["POST"])
def add_user():
    return users.add_user(db)

@app.route("/api/{version}/users/<int:id>".format(version=VERSION), methods=["PUT"])
def update_user(id):
    return users.update_user(id,db)

@app.route("/api/{version}/users".format(version=VERSION), methods=["GET"])
def get_users():
    return users.get_users(db)

@app.route("/api/{version}/users/<int:id>/".format(version=VERSION), methods=["GET"])
def get_user(id):
    return users.get_user(id,db)

@app.route("/api/{version}/users/<int:id>".format(version=VERSION), methods=["DELETE"])
def delete_user(id):
    return users.delete_user(id,db)


################################################################################
## Therapists CRUD Endpoints
################################################################################
@app.route("/api/{version}/therapists/".format(version=VERSION), methods=["POST"])
def add_therapist():
    return therapists.add_therapist(db)

@app.route("/api/{version}/therapists/<int:id>".format(version=VERSION), methods=["PUT"])
def update_therapist(id):
    return therapists.update_therapist(id,db)

@app.route("/api/{version}/therapists/".format(version=VERSION), methods=["GET"])
def get_therapists():
    return therapists.get_therapists(db)

@app.route("/api/{version}/therapists/<int:id>".format(version=VERSION), methods=["GET"])
def get_therapist(id):
    return therapists.get_therapist(id,db)

@app.route("/api/{version}/therapists/<int:id>".format(version=VERSION), methods=["DELETE"])
def delete_therapist(id):
    return delete_therapist(id,db)

if __name__ == "__main__":
    app.debug = True
    app.run()
