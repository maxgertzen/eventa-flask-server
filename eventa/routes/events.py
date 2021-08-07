from flask import Blueprint, request, Response, session
from flask_httpauth import HTTPBasicAuth
from eventa.models import Event
from eventa.utils import s_auth
import json


auth = HTTPBasicAuth()
events_route = Blueprint("events_route", __name__)


@events_route.route('/events', methods=["GET"])
def get_all_events():
    try:
        data = Event.objects(is_public=1)
        for event in data:
            event["_id"] = str(event["_id"])
        return Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "cannot get events"}),
            status=500,
            mimetype="application/json"
        )


@events_route.route('/events/dashboard', methods=["POST"])
@auth.login_required
def get_user_events():
    try:
        user_id = s_auth.loads(session['X-Authenticated'])
        print(user_id)
        data = Event.objects(user_host=user_id)
        if data.count():
            for event in data:
                event["_id"] = str(event["_id"])
            return Response(
                response=json.dumps(data),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({"message": "No user events"}),
                status=201,
                mimetype="application/json"
            )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "cannot get events"}),
            status=500,
            mimetype="application/json"
        )


@events_route.route('/events/<event_id>', methods=["GET", "PUT"])
@auth.login_required(optional=True)
def handle_event(event_id, data_to_update):
    try:
        if request.method == 'PUT' and auth.current_user():
            dbResponse = Event.objects(id=event_id).update_one(**dict(data_to_update))
            print(dbResponse)
            if dbResponse.modified_count == 1:
                return Response(
                    response=json.dumps({
                        "message": "event updated"
                    }),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    response=json.dumps({
                        "message": "Nothing to update"
                    }),
                    status=200,
                    mimetype="application/json"
                )
        elif request.method == 'GET':
            dbResponse = Event.objects(id=event_id)
            if dbResponse.count():
                return Response(
                    response=json.dumps({
                        "message": "event sent",
                        "data": dbResponse
                    }),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    response=json.dumps({
                        "message": "No such event"
                    }),
                    status=301,
                    mimetype="application/json"
                )
        else:
            return Response(
                response=json.dumps({
                    "message": "Something went wrong"
                }),
                status=501,
                mimetype="application/json"
            )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps(
                {"message": "sorry cannot update event"},
            ),
            status=500,
            mimetype="application/json"
        )


@events_route.route('/events/<event_id>', methods=["DELETE"])
@auth.login_required
def delete_event(event_id):
    try:
        query_event = Event.objects(id=event_id)
        user_id = s_auth.loads(session['X-Authenticated'])
        if user_id in query_event:
            dbResponse = query_event.delete()
            print(dbResponse)
            if dbResponse.deleted_count == 1:
                return Response(
                    response=json.dumps({
                        "message": "event deleted"
                    }),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    response=json.dumps({
                        "message": "Event not found"
                    }),
                    status=200,
                    mimetype="application/json"
                )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps(
                {"message": "sorry cannot delete event"},
            ),
            status=500,
            mimetype="application/json"
        )
