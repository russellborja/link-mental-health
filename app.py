from flask import Flask, render_template, request, jsonify
from flask_heroku import Heroku
from db.models import db, User, UserSchema

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/russellborja"
db.init_app(app)
# heroku = Heroku(app)

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

@app.route("/api/v1/users", methods=["POST"])
def add_user():
    body = request.get_json()

    email = body.get("email")
    username = body.get("username")
    phone_number = body.get("phone_number")
    notes = body.get("notes")

    if not username or not email:
        raise Error("Payload must contain username and e-mail attribute", 400)

    if not User.query.filter_by(username=username).count():
        reg = User(username, email, phone_number, notes)
        db.session.add(reg)
        db.session.commit()
        return jsonify({"message": "Succesfully added user."}), 200
    else:
        raise Error("User already in database", 400)
    raise Error("Could not save user to database", 500)

@app.route("/api/v1/users/<username>", methods=["GET"])
def get_user(username):
    try:
        user = User.query.filter_by(username=username).one()
        user_result = UserSchema().dump(user)
        print(bool(user_result.data))
        if user_result.errors:
            raise Error("Encountered errors retrieving user", 500, user_result.errors)
        return jsonify(user_result.data), 200
    except:
        raise Error("Could not find user", 404)

if __name__ == "__main__":
    app.debug = True
    app.run()