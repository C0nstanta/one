from ..db.models import Admin


class Authorization:

    secret_key = 'somesecretkeyhereitcanbeasahash'

    def __init__(self, login, password):
        self._login = login
        self._password = password

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, login):
        self._login = login

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    def check_log_pass_registration(self):
        admins = Admin.objects
        for admin in admins:
            if self._login == admin.username and self._password == admin.password:
                return True
        return False
