import sqlite3
import os


class MyDBManager:

    base_dir = "/Users/admin/Google Drive/Colab Notebooks/ITEA/7Lesson/"
    db_path = os.path.join(base_dir, "my_db7.db")

    def __init__(self, db):
        self._db = db

    def __enter__(self):
        self.conn = sqlite3.connect(self._db)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        if exc_val:
            raise Exception("Our error here")


class DBManager:

    db_path = MyDBManager.db_path

    def __init__(self, role, choice):
        self._role = role
        self._choice = choice

    def get_db_info(self):
        try:
            with MyDBManager(self.db_path) as conn:
                cursor = conn.cursor()
                res = cursor.execute("SELECT  fname, lname, stud_card_num, faculty, grades.Scores, grades.Subject, "
                                     "grades.Date FROM students  LEFT JOIN grades ON grades.student_id = students.id")
                print("Here is the full information about students.")
                for record in res:
                    print(record)
            return True, self._role
        except Exception as e:
            print(e)

    def add_student(self, fname, lname, stud_card_num, faculty):
        if self._role == 1:
            user_role = 2
            try:
                with MyDBManager(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO  students ('role', 'fname', 'lname', 'stud_card_num', 'faculty') "
                                   "VALUES (?, ?, ?, ?, ?)", (int(user_role), fname, lname, int(stud_card_num), faculty))
                    conn.commit()
                    print(f'{fname}:{lname} added to DB')
                    return True, 1
            except Exception as e:
                print(e)
        else:
            print("You cannot have admin access\n")
            return True, 2

    def get_by_id(self, stud_id):
        try:
            with MyDBManager(self.db_path) as conn:
                cursor = conn.cursor()
                row_query = "SELECT fname, lname, stud_card_num, faculty   FROM students where id = ?"
                value_query = (stud_id, )
                res = cursor.execute(row_query, value_query)
                print(res.fetchall())
            return True, self._role
        except Exception as e:
            print(e)

    def get_by_card(self, card_num):
        try:
            with MyDBManager(self.db_path) as conn:
                cursor = conn.cursor()
                row_query = "SELECT fname, lname, stud_card_num, faculty   FROM students where stud_card_num = ?"
                value_query = (card_num, )
                res = cursor.execute(row_query, value_query)
                print(res.fetchall())
            return True, self._role
        except Exception as e:
            print(e)

    def get_agrade(self, grade):
        try:
            with MyDBManager(self.db_path) as conn:
                cursor = conn.cursor()
                row_query = "SELECT  fname, lname, stud_card_num, faculty, grades.Scores, grades.Subject, grades.Date " \
                            "FROM students LEFT JOIN grades ON grades.student_id = students.id WHERE grades.Scores > ?"
                value_query = (grade, )
                res = cursor.execute(row_query, value_query)
                for record in res:
                    print(record)
            return True, self._role
        except Exception as e:
            print(e)

    def change_del_student(self):
        if self._role == 1:
            try:
                with MyDBManager(self.db_path) as conn:
                    cursor = conn.cursor()
                    res = cursor.execute("SELECT  id, fname, lname, stud_card_num, faculty FROM students ")
                    print("Here is the full information about students.")
                    for record in res:
                        print(record)
                change_choice = int(input("Do you want:\n1.Change student data\n2.Delete student\n3.Quit\n"))

                if change_choice == 1:
                    stud_id = int(input("Enter student id you want to change\n"))
                    with MyDBManager(self.db_path) as conn:
                        cursor = conn.cursor()
                        res = cursor.execute("SELECT * FROM students where id =?", (stud_id,))
                        print(res.fetchall())
                        fname = input("Enter student first name\n")
                        sname = input("Enter student surname\n")
                        stud_card_num = input("Enter student card number\n")
                        fac = input("Enter student faculty\n")

                        if fname.isalpha() and sname.isalpha() and stud_card_num.isnumeric() and fac.isalpha():
                            update_row ="UPDATE students set fname = ?, lname = ?, stud_card_num = ?, faculty = ? " \
                                        "where id = ?"
                            update_values = (fname, sname, stud_card_num, fac, stud_id)
                            cursor.execute(update_row, update_values)
                            conn.commit()
                            return True, self._role
                        else:
                            print("Try again\n")
                            return True, self._role

                if change_choice == 2:
                    stud_id = int(input("Enter student id you want delete\n"))
                    with MyDBManager(self.db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM students where id =?", (stud_id,))
                        conn.commit()
                    return True, self._role

                if change_choice == 3:
                    return True, self._role
            except Exception as e:
                print(e)