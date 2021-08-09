import json
from bson import ObjectId


class EventJSON:
    def __init__(self, *args, **kwargs):
        self.id = str(args["_id"])
        self.name = args["name"]
        self.description = args["description"]
        self.price = args["price"]
        self.dateStart = args["start_date"]
        self.dateEnd = args["end_date"]
        self.imageupload = args["image"]
        self.isPublic = args["is_public"]


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

