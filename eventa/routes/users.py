import os

from flask import Blueprint, request, Response, session
import json

from eventa.models import User
from eventa.utils import s_auth, UserFormatter

users_route = Blueprint("users_route", __name__)


@users_route.route('/dashboard', methods=["GET"])
def get_user_details():
    try:
        if request.cookies.get('user') and session["X-Authenticated"]:
            user_id = s_auth.loads(session['X-Authenticated'])
            dbResponse = User.objects(id=user_id).first()
            user = json.loads(dbResponse.to_json())
            user["_id"] = str(user["_id"]["$oid"])
            result = UserFormatter(**user)
            return Response(
                response=json.dumps(json.loads(result.to_json())),
                status=200,
                mimetype="application/json"
            )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Something went wrong"}),
            status=500,
            mimetype="application/json"
        )

