import os
from datetime import datetime

from bson import ObjectId
from flask import Blueprint, request, Response, session
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
from mongoengine.queryset.visitor import Q
from eventa.models import Event
from eventa.utils import s_auth, allowed_file, EventFormatter
import json


auth = HTTPBasicAuth()
events_route = Blueprint("events_route", __name__)


@events_route.route('/all', methods=["GET"])
def get_all_events():
    try:
        data = list()
        result = Event.objects(is_public=1).order_by('start_date') if 'search' not in request.args\
            else Event.objects(Q(is_public=1) & Q(start_date__gte=datetime.now()))\
            .order_by('start_date')
        if 'search' in request.args:
            result = result.limit(4)
        for single_event in result:
            single_event = json.loads(single_event.to_json())
            single_event["_id"] = str(single_event["_id"]["$oid"])
            new_e = EventFormatter(**single_event)
            data.append(json.loads(new_e.to_json()))
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


@events_route.route('/dashboard', methods=["GET"])
def get_user_events():
    try:
        data = list()
        if request.cookies.get('user'):
            user_id = s_auth.loads(session['X-Authenticated'])
            results = Event.objects(user_host=user_id)
            if results.count():
                for event in results:
                    event = json.loads(event.to_json())
                    event["_id"] = str(event["_id"]["$oid"])
                    new_e = EventFormatter(**event)
                    data.append(json.loads(new_e.to_json()))
                return Response(
                    response=json.dumps({"userEvents": data, "count": len(data)}),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    response=json.dumps({"message": "No user events"}),
                    status=201,
                    mimetype="application/json"
                )
        else:
            return Response(
                response=json.dumps({"message": "Unauthorized"}),
                status=400,
                mimetype="application/json"
            )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "cannot get events"}),
            status=500,
            mimetype="application/json"
        )


@events_route.route('/create', methods=["POST"])
@auth.login_required
def create_event():
    try:
        new_event = Event(**dict(request.values))
        file = request.files["imageupload"]
        valid_filename = allowed_file(file.filename)
        if file and valid_filename:
            filename = secure_filename(file.filename)
            image_path = os.path.join(os.environ["IMAGES_UPLOAD"], filename)
            new_event["image"] = image_path
            file.save(image_path)
        elif file and not valid_filename:
            return Response(
                response=json.dumps({"message": "Wrong image format, please upload different image"}),
                status=501,
                mimetype="application/json"
            )
        else:
            new_event["image"] = '/image-placeholder.png'
        new_event["user_host"] = s_auth.loads(session["X-Authenticated"])
        new_event.save()
        return Response(
            response=json.dumps({"message": f"Event {new_event.name} created"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Something went wrong with adding the event"}),
            status=500,
            mimetype="application/json"
        )


@events_route.route('/<event_id>', methods=["GET", "PUT"])
@auth.login_required(optional=True)
def handle_event(event_id, data_to_update=None):
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
            print(event_id)
            dbResponse = Event.objects(id=event_id).first()
            if dbResponse:
                result = json.loads(dbResponse.to_json())
                result["_id"] = str(result["_id"]["$oid"])
                formatted_e = EventFormatter(**result)
                return Response(
                    response=json.dumps(json.loads(formatted_e.to_json())),
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


@events_route.route('/<event_id>', methods=["DELETE"])
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
