import os
import mongoengine
from mongoengine import *
import datetime


connect(db="eventa", host=os.environ.get("DB_URI"))


class Category(Document):
    title = StringField()
    cat_code = IntField(required=True, unique=True)


class User(DynamicDocument):
    first_name = StringField(required=False)
    last_name = StringField(required=False)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    bio = StringField(required=False)
    birth_date = DateTimeField(default=datetime.datetime.now)
    image = StringField(required=False)
    address = StringField(required=False)
    accept_mail = IntField(min_value=0, max_value=1, default=0)
    is_verified = IntField(min_value=0, max_value=1, default=0)
    saved_events = ListField(StringField())

    meta: {
        'collections': 'user',
        'indexes': '$email'
    }


class Venue(Document):
    venueName = StringField(required=True)
    venue_ref = IntField(null=False)
    venueDescription = StringField()
    venueWebsite = URLField()
    street = StringField()
    city = StringField()
    country = StringField()


class Event(Document):
    name = StringField()
    description = StringField()
    price = IntField()
    start_date = DateTimeField(default=datetime.datetime.now)
    end_date = DateTimeField(default=datetime.datetime.now)
    is_public = IntField(default=0)
    guest_list = ListField(ReferenceField('User', reverse_delete_rule=mongoengine.NULLIFY))
    image = StringField()
    category = DictField()
    user_host = ReferenceField(User, required=True, reverse_delete_rule=mongoengine.NULLIFY)
    venue = DictField()
    venueName = StringField()
    venueStreet = StringField()
    venueCity = StringField()
    venueCountry = StringField()

    meta: {
        'collections': 'event',
        'indexes': [
            ('+category', '$name', '$description', '+start_date', '+is_public')
        ]
    }