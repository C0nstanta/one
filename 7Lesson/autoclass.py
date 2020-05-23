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
        try:
            with MyDBManager(db_path) as conn:
                cursor = conn.cursor()
                res = cursor.execute("SELECT login, pass, role FROM users")
                for record in res:
                    print(f'login:{record[0]},pass:{record[1]},role:{record[2]}')
                    if self._login == record[0] and self._password == record[1]:
                        print("Yes. You are in a base")
                        if record[2] == 1:
                            print("And you are: admin\n")
                            return True, 1
                        if record[2] == 2:
                            print("And you are: user\n")
                            return True, 2
                print("You are not in a base.\n")
                return False, 0
        except Exception as e:
            print(e)
