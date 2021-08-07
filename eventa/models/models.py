import os
import mongoengine
from mongoengine import *
import datetime


connect(db="eventa", host=os.environ.get("DB_URI"))


class Category(Document):
    title = StringField()
    cat_code = IntField(required=True, unique=True)


class User(Document):
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
    saved_events = ListField(ObjectIdField)

    meta: {
        'collections': 'user',
        'indexes': 'email'
    }


class Venue(Document):
    venueName = StringField(required=True)
    venueDescription = StringField()
    venueWebsite = URLField()
    street = StringField()
    city = StringField()
    country = StringField()


class Event(Document):
    name = StringField()
    description = StringField()
    price = IntField()
    date_start = DateTimeField(default=datetime.datetime.now)
    date_end = DateTimeField(default=datetime.datetime.now)
    is_public = BinaryField(default=0)
    guest_list = ListField(ReferenceField('User', reverse_delete_rule=mongoengine.NULLIFY))
    image = StringField()
    venue_id = ReferenceField('Venue', reverse_delete_rule=mongoengine.NULLIFY)
    user_host = ReferenceField('User', required=True, reverse_delete_rule=mongoengine.NULLIFY)
    category_id = ReferenceField('Category')

    meta: {
        'indexes': [
            ('+category_id', '$name', '$description')
        ]
    }