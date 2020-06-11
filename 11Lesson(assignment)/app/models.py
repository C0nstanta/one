import mongoengine as me
import datetime


me.connect('TeleShop')


class Users(me.Document):

    fname = me.StringField(min_length=2, max_length=256)
    mname = me.StringField(min_length=2, max_length=256)
    sname = me.StringField(min_length=2, max_length=256)
    phonenumber = me.StringField(min_length=2, max_length=256)
    email = me.StringField(min_length=2, max_length=256)
    address = me.StringField(min_length=2, max_length=256)
    comments = me.StringField(min_length=2, max_length=4096)
    created = me.DateTimeField(default=datetime.datetime.utcnow())

