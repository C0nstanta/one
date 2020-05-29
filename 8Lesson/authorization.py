from dbmanager import MyDBManager


class Authorization:

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

        db_path = MyDBManager.db_path
        with MyDBManager(db_path) as conn:
            cursor = conn.cursor()
            res = cursor.execute("SELECT login, pass FROM user")
            for record in res:
                print(f'login:{record[0]},pass:{record[1]}')
                if self._login == record[0] and self._password == record[1]:
                    print("Yes. You are in a base")
                    return True
                else:
                    return False


