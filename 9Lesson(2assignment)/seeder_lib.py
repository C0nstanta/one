import sqlite3
import os
import random


class MyDBManager():
    base_dir = os.getcwd()
    db_path = os.path.join(base_dir, "9lessondb2.db")

    def __init__(self, db):
        self._db = db

    def __enter__(self):
        self.conn = sqlite3.connect(self._db , check_same_thread=False)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        if exc_val:
            raise Exception("MyDBManager error!")


class DBManager(object):

    script_path = os.getcwd()
    file_path = script_path + '/randombase/'
    db_path = MyDBManager.db_path

    fname_list = []
    surname_list = []
    faculty_list = []
    used_fac = []

    def seed_faculty(self,num_seed):
        with open(self.file_path + 'faculty_names.txt', encoding='utf-8', mode='r') as fac_name:
            self.faculty_list = ([x.replace('\n','') for x in fac_name])

        with MyDBManager(self.db_path) as conn:
            i = 0
            while i < num_seed:
                cursor = conn.cursor()
                fac_rand = random.choice(self.faculty_list)

                if fac_rand not in self.used_fac:#проверяем на наличие совпадений среди добаленных факультетов.
                    row_query = f"INSERT INTO  faculty_tbl ('fac_name') VALUES (?)"
                    value_query = (fac_rand,)
                    cursor.execute(row_query, value_query)
                    conn.commit()
                    self.used_fac.append(fac_rand)
                    print(f'Faculty:{fac_rand} was added')
                    i += 1
                else:
                    continue

    def seed_curators(self,num_seed):
        with open(self.file_path + 'fname.txt', encoding='utf-8', mode='r') as fname:
            for name in fname:
                self.fname_list.append(name.replace('\n',''))

        with open(self.file_path + 'lname.txt', encoding='utf-8', mode='r') as sname:
            self.surname_list = [x.replace('\n','') for x in sname]

        with MyDBManager(self.db_path) as conn:
            i = 0
            while i < num_seed:
                cursor = conn.cursor()
                fname_rand = random.choice(self.fname_list)
                surname_rand = random.choice(self.surname_list)
                row_query = f"INSERT INTO  curators_tbl ('fname', 'lname') VALUES (?, ?)"
                value_query = (fname_rand, surname_rand)
                cursor.execute(row_query, value_query)
                conn.commit()
                print(f'Curator:{fname_rand} {surname_rand} was added')
                i += 1

    def seed_students(self, num_seed):

        curator_id_list = []
        faculty_id_list = []

        with open(self.file_path + 'fname.txt', encoding='utf-8', mode='r') as fname:
            for name in fname:
                self.fname_list.append(name.replace('\n',''))

        with open(self.file_path + 'lname.txt', encoding='utf-8', mode='r') as sname:
            self.surname_list = [x.replace('\n','') for x in sname]

        with MyDBManager(self.db_path) as conn:#Получаем id всех кураторов
            cursor = conn.cursor()
            res_cur = cursor.execute("SELECT id FROM curators_tbl")
            curator_id_list = [x[0] for x in res_cur.fetchall()]

        with MyDBManager(self.db_path) as conn:#Получаем id всех факультетов
            cursor = conn.cursor()
            res_fac = cursor.execute("SELECT id FROM faculty_tbl")
            faculty_id_list = [x[0] for x in res_fac.fetchall()]

        with MyDBManager(self.db_path) as conn:
            i = 0
            while i < num_seed:
                cursor = conn.cursor()
                fname_rand = random.choice(self.fname_list)
                surname_rand = random.choice(self.surname_list)
                fac_id_rand = random.choice(faculty_id_list)
                cur_id_rand = random.choice(curator_id_list)
                row_query = f"INSERT INTO  students_tbl ('fname', 'lname', 'curator_id', 'faculty_id') " \
                    f"VALUES (?, ?, ?, ?)"
                value_query = (fname_rand, surname_rand, cur_id_rand, fac_id_rand)
                cursor.execute(row_query, value_query)
                conn.commit()
                print(f'Student:{fname_rand} {surname_rand} was added')
                i += 1