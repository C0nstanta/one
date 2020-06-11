from .models import Users
from .schemas import TeleSchema
from marshmallow import ValidationError
import re
import json


class DBManager:

    user_dict = {}

    def get_fio(self, fio_str):
        pattern = '\w+'
        fio = re.findall(pattern, fio_str)
        try:
            self.user_dict['fname'] = str(fio[0])
            self.user_dict['mname'] = str(fio[1])
            self.user_dict['sname'] = str(fio[2])
            return True
        except IndexError as e:
            print(e)
        return False

    def get_phone(self, num):
        pattern = '\d+'
        phone = re.findall(pattern, num)
        try:
            self.user_dict['phonenumber'] = str(phone[0])
            return True
        except IndexError as e:
            print(e)
        return False

    def get_email(self, email_raw):
        pattern = '[\w\-_\..]+@[\w]+.[\w]{2,3}'
        try:
            email = re.findall(pattern, email_raw)
            self.user_dict['email'] = str(email[0])
            return True
        except IndexError as e:
            print(e)
        return False

    def get_address(self, address_raw):
        try:
            self.user_dict['address'] = str(address_raw)
            return True
        except IndexError as e:
            print(e)
        return False

    def get_comment(self, raw_comment):
        try:
            self.user_dict['comments'] = str(raw_comment)
            self.write_to_db()
            return True
        except IndexError as e:
            print(e)
        return False

    def write_to_db(self):
        data = TeleSchema().loads(json.dumps(self.user_dict))
        print(data)
        try:
            Users.objects.create(**data)
        except ValidationError as e:
            print(e)