from .models import Users, Status, TempData
from .schemas import TeleSchema
from marshmallow import ValidationError
import re
import json


class DBManager:

    user_dict = {}

    def check_status(self, chat_id):
        print(f'message.chat.id:{chat_id}')
        for status in Status.objects:
            if str(chat_id) == status.user_chat_id:
                stat_id = status.user_status
                return stat_id
        else:
            Status.objects.create(user_status=1, user_chat_id=str(chat_id))
            return 1

    def temp_data(self, chat_id, status):
        if status != 1 and status != 0:
            for status in Status.objects(user_chat_id=str(chat_id)):
                temp_id = status.id
                for temp in TempData.objects(status=temp_id):
                    self.user_dict['fname'] = temp.temp_fname
                    self.user_dict['mname'] = temp.temp_mname
                    self.user_dict['sname'] = temp.temp_sname
                    self.user_dict['phonenumber'] = temp.temp_phonenumber
                    self.user_dict['email'] = temp.temp_email
                    self.user_dict['address'] = temp.temp_address
                    self.user_dict['comments'] = temp.temp_comments
        else:
            return

    def temp_drop_doc(self, chat_id):
        for status in Status.objects(user_chat_id=str(chat_id)):
            temp_id = status.id
            TempData.objects(status=temp_id).delete()

    def get_fio(self, fio_str, chat_id):
        pattern = '\w+'
        fio = re.findall(pattern, fio_str)
        try:
            self.user_dict['fname'] = str(fio[0])
            self.user_dict['mname'] = str(fio[1])
            self.user_dict['sname'] = str(fio[2])

            for status in Status.objects(user_chat_id=str(chat_id)):
                TempData.objects.create(status=status.id, temp_fname=self.user_dict['fname'],
                                        temp_mname=self.user_dict['mname'], temp_sname=self.user_dict['sname'],
                                        temp_phonenumber="", temp_email="", temp_address="", temp_comments="")
            Status.objects(user_chat_id=str(chat_id)).update(user_status=2)
            return True
        except IndexError as e:
            print(e)
        return False

    def get_phone(self, num, chat_id):
        pattern = '\d+'
        phone = re.findall(pattern, num)
        try:
            self.user_dict['phonenumber'] = str(phone[0])
            for status in Status.objects(user_chat_id=str(chat_id)):
                TempData.objects(status=status.id).update(temp_phonenumber=self.user_dict['phonenumber'])

            Status.objects(user_chat_id=str(chat_id)).update(user_status=3)
            return True
        except IndexError as e:
            print(e)
        return False

    def get_email(self, email_raw, chat_id):
        pattern = '[\w\-_\..]+@[\w]+.[\w]{2,3}'
        try:
            email = re.findall(pattern, email_raw)
            self.user_dict['email'] = str(email[0])
            for status in Status.objects(user_chat_id=str(chat_id)):
                TempData.objects(status=status.id).update(temp_email=self.user_dict['email'])

            Status.objects(user_chat_id=str(chat_id)).update(user_status=4)
            return True
        except IndexError as e:
            print(e)
        return False

    def get_address(self, address_raw, chat_id):
        try:
            self.user_dict['address'] = str(address_raw)
            for status in Status.objects(user_chat_id=str(chat_id)):
                TempData.objects(status=status.id).update(temp_address=self.user_dict['address'])

            Status.objects(user_chat_id=str(chat_id)).update(user_status=5)
            return True
        except IndexError as e:
            print(e)
        return False

    def get_comment(self, raw_comment, chat_id):
        try:
            self.user_dict['comments'] = str(raw_comment)
            self.write_to_db(chat_id)
            for status in Status.objects(user_chat_id=str(chat_id)):
                TempData.objects(status=status.id).update(temp_comments=self.user_dict['comments'])

            Status.objects(user_chat_id=str(chat_id)).update(user_status=6)
            return True
        except IndexError as e:
            print(e)
        return False

    def write_to_db(self, chat_id):
        data = TeleSchema().loads(json.dumps(self.user_dict))
        try:
            for status in Status.objects(user_chat_id=str(chat_id)):
                Users.objects.create(status=status.id, **data)
        except ValidationError as e:
            print(e)