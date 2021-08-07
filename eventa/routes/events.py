from flask import Blueprint, request, Response, session
import json
from eventa.models import Event


events_route = Blueprint("events_route", __name__)


@events_route.route('/events', methods=["GET"])
def get_some_events():
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


@events_route.route('/events/<event_id>', methods=["PUT"])
# login_required
def update_event(event_id, data_to_update):
    try:
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
# login_required
def delete_event(event_id):
    try:
        query_event = Event.objects(id=event_id)
        if session["user_id"] in query_event:
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
