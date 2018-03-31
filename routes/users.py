from flask import request, jsonify
from db.models import User, UserSchema
from utils.error import bad_request, not_found


def add_user(db):
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

def update_user(id,db):
    body = request.get_json()
    payload = {}
    for column in User.__table__.columns:
        column_name = str(column).split(".")[1]
        if column_name != "user_id":
            payload[column_name] = body.get(column_name)

    if not payload["username"] or not payload["email"]:
        return bad_request("Username and e-mail must be provided")

    try:
        user = User.query.get(id)
        if user.username != payload["username"] and User.query.filter_by(username=payload["username"]).count():
            return bad_request("Username already exists, select another username")

        for key, val in payload.items():
            setattr(user, key, val)

        user_updated = UserSchema().dump(user)
        db.session.commit()
        return jsonify(user_updated.data), 201
    except:
        return not_found("Could not find user with given ID")

def get_users(db):
    response = {
        "users": []
    }
    users = User.query.all()
    for user in users:
        user_obj = UserSchema().dump(user)
        response["users"].append(user_obj.data)
    return jsonify(response)

def get_user(id,db):
    try:
        user = User.query.filter_by(user_id=id).first_or_404()
        user_result = UserSchema().dump(user)
        return jsonify(user_result.data)
    except:
        return not_found("Could not find user with given ID")

def delete_user(id,db):
    user = User.query.get(id)
    if user:
        username = user.username
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Successfully deleted {user}".format(user=username)}), 200
    else:
        return bad_request("User does not exist")
