import json
import datetime
from bson import Timestamp


def datetime_option(value):
    if isinstance(value, datetime.date):
        return value.isoformat()
    else:
        return value.__dict__


class EventFormatter:
    def __init__(self, **kwargs):
        self.event_id = kwargs.get('_id')
        self.eventName = kwargs.get('name')
        self.description = kwargs.get('description')
        self.categoryName = kwargs.get('category')["title"]
        self.venueName = kwargs.get('venueName')
        self.address = kwargs.get('venueStreet')
        self.city = kwargs.get('venueCity')
        self.country = kwargs.get('venueCountry')
        self.dateStart = Timestamp(kwargs.get('start_date')["$date"] // 1000, 1).as_datetime()
        self.dateEnd = Timestamp(kwargs.get('end_date')["$date"] // 1000, 1).as_datetime()
        self.image = 'http://localhost:5050/static/' + kwargs.get('image')
        allowed_refs = ['user_host', 'is_public', 'venue']
        for key in allowed_refs:
            v = kwargs.get(key, None)
            value = v.get('venue_ref') if key == 'venue' else v
            setattr(self, key, value)

    def to_json(self):
        return json.dumps(self, default=datetime_option, sort_keys=True, indent=4)


class UserFormatter:
    def __init__(self, **kwargs):
        self.user_id = kwargs.get('_id')
        self.email = kwargs.get('email')
        self.bio = kwargs.get('bio')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.birth_date = Timestamp(kwargs.get('birth_date')["$date"] // 1000, 1).as_datetime()
        self.accept_mail = kwargs.get('accept_mail')
        self.city = kwargs.get('city')
        self.country = kwargs.get('country')
        self.image = 'http://localhost:5050/static/images' + kwargs.get('image')

    def to_json(self):
        return json.dumps(self, default=datetime_option, sort_keys=True, indent=4)