import os

from flask import Blueprint, request, Response, session
import json

from eventa.models import User
from eventa.utils import s_auth


users_route = Blueprint("users_route", __name__)


@users_route.route('/register', methods=["POST"])
def create_user():
    try:
        new_user = dict(request.values)
        new_user["password"] = s_auth.dumps(new_user["password"])
        dbResponse = User(**new_user)
        dbResponse.save()
        os.environ["PASS_HASH"] = generate_password_hash(new_user["password"])
        session['X-Authenticated'] = s_auth.dumps(str(dbResponse.id))
        session['user'] = s_auth.dumps(dbResponse.first_name)
        res = Response(
            response=json.dumps({"message": "user created", "id": f"{dbResponse.id}"}),
            status=200,
            mimetype="application/json"
        )
        res.set_cookie("user", f"{dbResponse.id}?{dbResponse.first_name}")
        return res
    except Exception as ex:
        msg = 'Email already registered' if type(ex) is mongoengine.errors.NotUniqueError else 'Something went wrong'
        return Response(
            response=json.dumps({"message": msg}),
            status=500,
            mimetype="application/json"
        )

