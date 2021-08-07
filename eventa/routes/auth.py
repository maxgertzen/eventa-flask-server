import os

import mongoengine
from flask import Blueprint, request, Response, session
import json
from werkzeug.security import generate_password_hash, check_password_hash

from eventa.models import User
from eventa.utils import s_auth


auth_route = Blueprint("auth_route", __name__)


@auth_route.route('/register', methods=["POST"])
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


@auth_route.route('/login', methods=["POST"])
def login_user():
    try:
        query = User.objects(email=request.values["email"])
        SECRET = os.environ.get("PASS_HASH", generate_password_hash(s_auth.dumps(query[0].password)))
        if query.count():
            print(query[0].password)
            if check_password_hash(SECRET, query[0].password):
                session["X-Authenticated"] = s_auth.dumps(str(query[0].id))
                return Response(
                    response=json.dumps({"message": "Logged In"}),
                    status=200,
                    mimetype="application/json"
                )
            session["X-Authenticated"] = None
            session.modified = True
        res = Response(
            response=json.dumps({"message": "Email or password is wrong"}),
            status=400,
            mimetype="application/json"
        )
        if query.count():
            res.set_cookie("user", f"{query[0].id}?{query[0].first_name}")
        return res
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Something went wrong"}),
            status=500,
            mimetype="application/json"
        )


@auth_route.route('logout', methods=["POST"])
def logout_user():
    session.clear()
    session.modified = True
    os.environ["PASS_HASH"] = ''
    return Response(
        response=json.dumps({"message": "Logged out"}),
        status=201,
        mimetype="application/json"
    )
