from flask import request, jsonify
from db.models import Therapist, TherapistSchema
from utils.error import bad_request, not_found


def add_therapist(db):
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

def update_therapist(id,db):
    body = request.get_json()
    payload = {}
    for column in Therapist.__table__.columns:
        column_name = str(column).split(".")[1]
        if column_name != "therapist_id":
            payload[column_name] = body.get(column_name)

    if not payload["name"] or not payload["specialty"] or not payload["location"]:
        return bad_request("Name, location, and specialty must be provided")

    therapist = Therapist.query.get(id)
    print(therapist)
    print(payload)
    if therapist.name != payload["name"] and Therapist.query.filter_by(name=payload["name"]).count():
        return bad_request("Therapist already exists, select another name")

    for key, val in payload.iteritems():
        setattr(therapist, key, val)
    therapist_updated = TherapistSchema().dump(therapist)
    print(therapist_updated.data)
    db.session.commit()
    return jsonify(therapist_updated.data), 201

def get_therapists(db):
    response = {
        "therapists": []
    }
    therapists = Therapist.query.all()
    for therapist in therapists:
        therapist_obj = TherapistSchema().dump(therapist)
        response["therapists"].append(therapist_obj.data)
    return jsonify(response)

def get_therapist(id,db):
    try:
        therapist = Therapist.query.filter_by(therapist_id=id).first_or_404()
        therapist_result = TherapistSchema().dump(therapist)
        return jsonify(therapist_result.data)
    except:
        return not_found("Could not find therapist with given ID")

def delete_therapist(id,db):
    therapist = Therapist.query.get(id)
    if therapist:
        name = therapist.name
        db.session.delete(therapist)
        db.session.commit()
        return jsonify({"message": "Successfully deleted {therapist}".format(therapist=name)}), 200
    else:
        return bad_request("Therapist does not exist")
