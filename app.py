from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/russellborja'
heroku = Heroku(app)
db = SQLAlchemy(app)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    notes = db.Column(db.String(120))

    def __init__(self, email, phone_number, notes):
        self.email = email
        self.phone_number = phone_number
        self.notes = notes

    def __repr__(self):
        return '<E-mail %r>' % self.email

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

# Set "homepage" to index.html
@app.route('/')
def index():
    return render_template('index.html')

# Save e-mail to database and send to success page
@app.route('/api/v1/users', methods=['POST'])
def add_user():
    email = None
    phone_number = None
    notes = None

    if request.method == 'POST':
        body = request.get_json()
        if 'email' not in body:
            raise InvalidUsage('Payload must contain e-mail attribute', 400)
        email = body['email']
        if 'phone_number' in body:
            phone_number = body['phone_number']
        if 'notes' in body:
            notes = body['notes']

        if not db.session.query(User).filter(User.email == email).count():
            reg = User(email, phone_number, notes)
            db.session.add(reg)
            db.session.commit()
            return "Succesfully added user."
        #     return render_template('success.html')
    return "Error: Did not save to db."

if __name__ == '__main__':
    app.debug = True
    app.run()