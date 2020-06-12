import mongoengine as me
import datetime


me.connect('TeleShop')


class Status(me.Document):
    user_status = me.IntField(required=True)
    user_chat_id = me.StringField(required=True)


class TempData(me.Document):
    status = me.ReferenceField(Status)

    temp_fname = me.StringField(max_length=256)
    temp_mname = me.StringField(max_length=256)
    temp_sname = me.StringField(max_length=256)
    temp_phonenumber = me.StringField(max_length=256)
    temp_email = me.StringField(max_length=256)
    temp_address = me.StringField(max_length=256)
    temp_comments = me.StringField(max_length=4096)


class Users(me.Document):

    status = me.ReferenceField(Status)

    fname = me.StringField(min_length=2, max_length=256)
    mname = me.StringField(min_length=2, max_length=256)
    sname = me.StringField(min_length=2, max_length=256)
    phonenumber = me.StringField(min_length=2, max_length=256)
    email = me.StringField(min_length=2, max_length=256)
    address = me.StringField(min_length=2, max_length=256)
    comments = me.StringField(min_length=2, max_length=4096)
    created = me.DateTimeField(default=datetime.datetime.utcnow())


if __name__ == "__main__":
    status = Status.objects.create(user_status=1, user_chat_id="somekeyid")
    Users.objects.create(status=status, fname="Fname", mname="Mname", sname="Sname", phonenumber="1123",
                         email="wdjfhie@djs.net", address="address1", comments="comments")